from __future__ import annotations

import streamlit as st

from quiz.api import CONTESTANTS, ContestantResult, healthcheck, race_contestants
from quiz.questions import Question, load_questions
from quiz.styles import (
    end_card_html,
    hero_html,
    inject,
    podium_html,
    podium_row_html,
    question_card_html,
    score_strip_html,
)

st.set_page_config(
    page_title="MongoDB RAG Quiz Show",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _init_state(question_count: int) -> None:
    st.session_state.setdefault("q_index", 0)
    st.session_state.setdefault("results", None)
    st.session_state.setdefault("revealed", False)
    st.session_state.setdefault("scored_questions", [])
    st.session_state.setdefault("scores", [0] * len(CONTESTANTS))
    st.session_state.setdefault("show_over", False)
    st.session_state.setdefault("flush_ui", False)
    st.session_state.setdefault("question_count", question_count)


def _reset_show() -> None:
    st.session_state.q_index = 0
    st.session_state.results = None
    st.session_state.revealed = False
    st.session_state.scored_questions = []
    st.session_state.scores = [0] * len(CONTESTANTS)
    st.session_state.show_over = False
    st.session_state.flush_ui = False


def _stored_results() -> list[ContestantResult] | None:
    raw = st.session_state.results
    if raw is None:
        return None
    return [ContestantResult.from_dict(item) for item in raw]


def _tile_state(result: ContestantResult | None, revealed: bool, correct: str) -> str:
    if result is None:
        return "waiting"
    if result.error or not result.letter:
        return "error"
    if not revealed:
        return "answered"
    return "correct" if result.letter == correct else "wrong"


def _apply_scores(question: Question, results: list[ContestantResult]) -> None:
    scored: list[int] = st.session_state.scored_questions
    if question.number in scored:
        return
    scores: list[int] = st.session_state.scores
    for index, result in enumerate(results):
        if result.letter == question.correct:
            scores[index] += 1
    scored.append(question.number)


@st.cache_data(ttl=8)
def _api_ok() -> bool:
    return healthcheck()


def _render_reference_docs(results: list[ContestantResult]) -> None:
    st.markdown('<p class="docs-heading">Reference docs</p>', unsafe_allow_html=True)
    tabs = st.tabs([contestant.name for contestant in CONTESTANTS])
    for tab, result in zip(tabs, results):
        with tab:
            if result.error:
                st.error(result.error)
            docs = result.reference_docs
            if not docs:
                st.caption("No retrieved chunks.")
                continue
            for doc_index, chunk in enumerate(docs, start=1):
                st.markdown(f"**Chunk {doc_index}**")
                st.markdown(chunk)
                if doc_index < len(docs):
                    st.divider()


def _podium_row(
    results: list[ContestantResult | None],
    revealed: bool,
    correct: str,
) -> str:
    cells = []
    for contestant, result in zip(CONTESTANTS, results):
        state = _tile_state(result, revealed, correct)
        cells.append(
            podium_html(
                contestant.name,
                contestant.caption,
                result.letter if result else None,
                state,
                result.error if result else None,
                result.input_tokens if result else None,
            )
        )
    return podium_row_html(cells)


def _paint_podiums(
    slot,
    question: Question,
    stored: list[ContestantResult] | None,
    revealed: bool,
) -> None:
    row = [None] * len(CONTESTANTS) if stored is None else list(stored)
    slot.html(_podium_row(row, revealed and stored is not None, question.correct))


def _fetch_answers(question: Question, slot) -> None:
    in_flight: list[ContestantResult | None] = [None] * len(CONTESTANTS)

    def _on_complete(index: int, result: ContestantResult) -> None:
        in_flight[index] = result
        slot.html(_podium_row(in_flight, False, question.correct))

    stored = race_contestants(question.prompt, on_complete=_on_complete)
    st.session_state.results = [item.to_dict() for item in stored]
    st.rerun()


def _render_end() -> None:
    scores: list[int] = st.session_state.scores
    best = max(scores) if scores else 0
    winners = [
        contestant.name
        for contestant, score in zip(CONTESTANTS, scores)
        if score == best and best > 0
    ]
    if winners:
        winner_line = (
            f"{' & '.join(winners)} topped the board with {best} "
            f"correct answer{'s' if best != 1 else ''}."
        )
    else:
        winner_line = (
            "No contestant landed a correct answer this round — retrieval still matters."
        )

    st.html(end_card_html(winner_line))
    st.html(score_strip_html([c.name for c in CONTESTANTS], scores))
    _, center, _ = st.columns([2, 1, 2])
    with center:
        if st.button("Restart the show", type="primary", use_container_width=True):
            _reset_show()
            st.rerun()


def main() -> None:
    questions = load_questions()
    _init_state(len(questions))
    st.markdown(inject(), unsafe_allow_html=True)
    api_ok = _api_ok()

    if st.session_state.show_over:
        st.html(hero_html(len(questions) - 1, len(questions), api_ok))
        _render_end()
        return

    q_index = int(st.session_state.q_index)
    question = questions[q_index]
    current_results = _stored_results()
    if st.session_state.revealed and current_results is not None:
        _apply_scores(question, current_results)

    st.html(hero_html(q_index, len(questions), api_ok))
    st.html(
        question_card_html(
            question.number,
            question.stem,
            question.options,
            correct=question.correct,
            revealed=bool(st.session_state.revealed),
        )
    )
    st.html(score_strip_html([c.name for c in CONTESTANTS], st.session_state.scores))

    stored = _stored_results()
    revealed = bool(st.session_state.revealed)

    with st.container(key="contestants"):
        podium_slot = st.empty()
        _paint_podiums(podium_slot, question, stored, revealed)

    all_replied = stored is not None
    is_last = q_index >= len(questions) - 1
    with st.container(key="quiz-actions"):
        reveal_col, next_col = st.columns(2)
        with reveal_col:
            reveal_clicked = st.button(
                "Reveal answer",
                type="primary",
                disabled=not all_replied or revealed,
                use_container_width=True,
                key="page-reveal",
            )
        with next_col:
            next_clicked = st.button(
                "Next question",
                type="primary",
                disabled=not revealed,
                use_container_width=True,
                key="page-next",
            )
    if reveal_clicked:
        st.session_state.revealed = True
        st.rerun()
    if next_clicked:
        if is_last:
            st.session_state.show_over = True
        else:
            st.session_state.q_index = q_index + 1
            st.session_state.results = None
            st.session_state.revealed = False
            st.session_state.flush_ui = True
        st.rerun()

    with st.container(key="reference-docs"):
        if stored is not None:
            _render_reference_docs(stored)
        else:
            st.html('<div class="docs-placeholder"></div>')

    if stored is None:
        if st.session_state.pop("flush_ui", False):
            st.rerun()
        _fetch_answers(question, podium_slot)


if __name__ == "__main__":
    main()
else:
    main()
