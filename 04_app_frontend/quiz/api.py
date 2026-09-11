from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable

import httpx

DEFAULT_API_BASE_URL = "http://localhost:8080"
REQUEST_TIMEOUT_SECONDS = 120.0


@dataclass(frozen=True)
class Contestant:
    id: str
    name: str
    caption: str
    use_rag: bool
    use_hybrid: bool
    use_reranker: bool


CONTESTANTS: tuple[Contestant, ...] = (
    Contestant(
        id="llm",
        name="LLM",
        caption="No retrieval. The model answers from training data only.",
        use_rag=False,
        use_hybrid=False,
        use_reranker=False,
    ),
    Contestant(
        id="vector",
        name="vector search -> LLM",
        caption="RAG with MongoDB vector search, 10 chunks output.",
        use_rag=True,
        use_hybrid=False,
        use_reranker=False,
    ),
    Contestant(
        id="hybrid",
        name="hybrid search -> LLM",
        caption="RAG combining vector and lexical search, 10 chunks output.",
        use_rag=True,
        use_hybrid=True,
        use_reranker=False,
    ),
    Contestant(
        id="reranker",
        name="hybrid + reranker -> LLM",
        caption="Hybrid retrieval producing 25 results, then the reranker sorts and limits the output to 5 chunks.",
        use_rag=True,
        use_hybrid=True,
        use_reranker=True,
    ),
)


def _parse_input_tokens(data: dict) -> int | None:
    raw = data.get("input_tokens")
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


@dataclass
class ContestantResult:
    letter: str | None = None
    reference_docs: list[str] = field(default_factory=list)
    error: str | None = None
    input_tokens: int | None = None

    def to_dict(self) -> dict:
        return {
            "letter": self.letter,
            "reference_docs": self.reference_docs,
            "error": self.error,
            "input_tokens": self.input_tokens,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ContestantResult":
        return cls(
            letter=data.get("letter"),
            reference_docs=list(data.get("reference_docs") or []),
            error=data.get("error"),
            input_tokens=_parse_input_tokens(data),
        )


def api_base_url() -> str:
    return os.environ.get("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


def healthcheck(base_url: str | None = None, timeout: float = 2.0) -> bool:
    url = f"{base_url or api_base_url()}/healthcheck"
    try:
        response = httpx.get(url, timeout=timeout)
        return response.status_code == 200
    except httpx.HTTPError:
        return False


def _ask_contestant(
    contestant: Contestant,
    question: str,
    base_url: str,
    timeout: float,
) -> ContestantResult:
    url = f"{base_url}/answer_question"
    payload = {
        "question": question,
        "use_rag": contestant.use_rag,
        "use_hybrid": contestant.use_hybrid,
        "use_reranker": contestant.use_reranker,
    }
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException:
        return ContestantResult(error="Timed out waiting for the API")
    except httpx.ConnectError:
        return ContestantResult(error=f"Could not connect to {base_url}")
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:180] if exc.response is not None else str(exc)
        return ContestantResult(error=f"API {exc.response.status_code}: {detail}")
    except httpx.HTTPError as exc:
        return ContestantResult(error=str(exc))
    except ValueError:
        return ContestantResult(error="API returned invalid JSON")

    letter = str(data.get("llm_answer") or "").strip().upper()
    input_tokens = _parse_input_tokens(data)
    if letter not in {"A", "B", "C", "D"}:
        return ContestantResult(
            error=f"Unexpected answer {letter!r}",
            reference_docs=list(data.get("reference_docs") or []),
            input_tokens=input_tokens,
        )

    return ContestantResult(
        letter=letter,
        reference_docs=list(data.get("reference_docs") or []),
        input_tokens=input_tokens,
    )


def race_contestants(
    question: str,
    on_complete: Callable[[int, ContestantResult], None],
    base_url: str | None = None,
    timeout: float = REQUEST_TIMEOUT_SECONDS,
) -> list[ContestantResult]:
    """Call all four scenarios in parallel. `on_complete` fires as each returns."""
    host = base_url or api_base_url()
    results: list[ContestantResult | None] = [None] * len(CONTESTANTS)

    with ThreadPoolExecutor(max_workers=len(CONTESTANTS)) as executor:
        futures = {
            executor.submit(_ask_contestant, contestant, question, host, timeout): index
            for index, contestant in enumerate(CONTESTANTS)
        }
        for future in as_completed(futures):
            index = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # noqa: BLE001 — keep the quiz running
                result = ContestantResult(error=str(exc))
            results[index] = result
            on_complete(index, result)

    return [item if item is not None else ContestantResult(error="No response") for item in results]
