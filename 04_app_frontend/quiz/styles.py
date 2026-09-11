from __future__ import annotations

import html
import textwrap

CSS = """
@import url("https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&display=swap");

:root {
  --mdb-black: #001E2B;
  --mdb-green: #00ED64;
  --mdb-evergreen: #00684A;
  --mdb-forest: #023430;
  --mdb-card: #112733;
  --mdb-card-2: #1a3644;
  --mdb-text: #E8EDEB;
  --mdb-muted: #C1C7C6;
  --mdb-border: #3D4F58;
  --mdb-yellow: #FFC010;
  --mdb-blue: #0498EC;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
  background: var(--mdb-black) !important;
  color: var(--mdb-text);
  font-family: "Figtree", "Helvetica Neue", Arial, sans-serif;
}

.stApp {
  background:
    radial-gradient(900px 420px at 8% -10%, rgba(0, 237, 100, 0.16), transparent 55%),
    radial-gradient(700px 380px at 108% 8%, rgba(4, 152, 236, 0.12), transparent 50%),
    radial-gradient(600px 400px at 70% 120%, rgba(0, 104, 74, 0.35), transparent 55%),
    var(--mdb-black) !important;
}

[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stHeader"],
#MainMenu,
header[data-testid="stHeader"],
footer,
.stDeployButton {
  display: none !important;
  visibility: hidden !important;
}

.block-container {
  padding-top: 1.4rem !important;
  padding-bottom: 3rem !important;
  max-width: 1280px !important;
}

h1, h2, h3, .show-title {
  font-family: "Source Serif 4", Georgia, serif !important;
}

.hero {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 1.25rem;
}

.hero-brand {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.eyebrow {
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--mdb-green);
  font-weight: 700;
  margin: 0 0 0.15rem 0;
}

.show-title {
  font-size: 2.15rem;
  line-height: 1.05;
  margin: 0;
  font-weight: 600;
  color: #ffffff;
}

.show-sub {
  margin: 0.35rem 0 0 0;
  color: var(--mdb-muted);
  font-size: 0.98rem;
}

.hero-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.45rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid var(--mdb-border);
  background: rgba(17, 39, 51, 0.85);
  color: var(--mdb-text);
  border-radius: 999px;
  padding: 0.28rem 0.7rem;
  font-size: 0.78rem;
  font-weight: 600;
}

.badge .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--mdb-green);
  box-shadow: 0 0 8px rgba(0, 237, 100, 0.8);
}

.badge.down .dot {
  background: #f87171;
  box-shadow: 0 0 8px rgba(248, 113, 113, 0.8);
}

.question-card {
  background: linear-gradient(180deg, rgba(26, 54, 68, 0.92), rgba(17, 39, 51, 0.92));
  border: 1px solid rgba(0, 237, 100, 0.18);
  border-radius: 18px;
  padding: 1.35rem 1.5rem 1.2rem 1.5rem;
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
  margin-bottom: 0.35rem;
}

.q-kicker {
  color: var(--mdb-green);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 0.72rem;
  margin-bottom: 0.55rem;
}

.q-stem {
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 1.45rem;
  line-height: 1.35;
  color: #fff;
  margin: 0 0 1rem 0;
}

.options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.65rem;
}

.option {
  display: flex;
  gap: 0.7rem;
  align-items: flex-start;
  background: rgba(0, 30, 43, 0.55);
  border: 1px solid var(--mdb-border);
  border-radius: 12px;
  padding: 0.7rem 0.8rem;
}

.option-letter {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: var(--mdb-green);
  color: var(--mdb-black);
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.option-text {
  color: var(--mdb-text);
  font-size: 0.92rem;
  line-height: 1.35;
  padding-top: 0.2rem;
}

.option.correct {
  background: var(--mdb-green);
  border-color: var(--mdb-green);
}

.option.correct .option-text {
  color: var(--mdb-black);
  font-weight: 700;
}

.option.correct .option-letter {
  background: var(--mdb-black);
  color: var(--mdb-green);
}

.score-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.6rem;
  margin: 0.9rem 0 1.1rem 0;
}

.score-pill {
  background: var(--mdb-card);
  border: 1px solid var(--mdb-border);
  border-radius: 12px;
  padding: 0.45rem 0.7rem;
  text-align: center;
}

.score-pill .label {
  color: var(--mdb-muted);
  font-size: 0.7rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-weight: 600;
}

.score-pill .value {
  color: var(--mdb-green);
  font-size: 1.15rem;
  font-weight: 800;
}

.podium-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.6rem;
  margin-bottom: 0.4rem;
}

.podium-wrap {
  display: flex;
  flex-direction: column;
}

.podium-head {
  background: var(--mdb-card);
  border: 1px solid var(--mdb-border);
  border-radius: 14px 14px 0 0;
  padding: 0.85rem 0.85rem 0.7rem 0.85rem;
  min-height: 96px;
}

.podium-name {
  font-weight: 800;
  font-size: 0.98rem;
  color: #fff;
  margin: 0 0 0.3rem 0;
  line-height: 1.2;
}

.podium-caption {
  color: var(--mdb-muted);
  font-size: 0.78rem;
  line-height: 1.35;
  margin: 0;
}

.answer-tile {
  border-radius: 0 0 14px 14px;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.2rem;
  padding: 0.55rem 0.5rem 0.7rem 0.5rem;
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 700;
  letter-spacing: 0.04em;
  border: 1px solid var(--mdb-border);
  border-top: none;
  margin-bottom: 0.7rem;
}

.answer-letter {
  font-size: 5.1rem;
  line-height: 1;
}

.token-count {
  font-family: "Figtree", sans-serif;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  line-height: 1.25;
  text-align: center;
  opacity: 0.82;
}

.answer-tile.waiting {
  background: #0b232e;
  color: #5c6c75;
  animation: pulse 1.4s ease-in-out infinite;
}

.answer-tile.answered {
  background: var(--mdb-yellow);
  color: #000000;
}

.answer-tile.correct {
  background: var(--mdb-green);
  color: #001E2B;
}

.answer-tile.wrong {
  background: #000000;
  color: #E8EDEB;
  border-color: #000000;
}

.answer-tile.error {
  background: #1b1214;
  color: #f87171;
  letter-spacing: 0.08em;
}

.answer-tile.error .answer-letter {
  font-size: 1.7rem;
}

.tile-error {
  font-family: "Figtree", sans-serif;
  font-size: 0.78rem;
  color: #fca5a5;
  text-align: center;
  margin: -0.45rem 0 0.7rem 0;
}

.end-card {
  background: var(--mdb-card);
  border: 1px solid rgba(0, 237, 100, 0.25);
  border-radius: 18px;
  padding: 2rem 1.6rem;
  text-align: center;
}

.end-card h2 {
  margin: 0.3rem 0 0.6rem 0;
  font-size: 2rem;
  color: #fff;
}

.end-card p {
  color: var(--mdb-muted);
  margin-bottom: 1.2rem;
}

div.stButton > button {
  background: var(--mdb-green) !important;
  color: var(--mdb-black) !important;
  border: none !important;
  border-radius: 24px !important;
  font-weight: 700 !important;
  font-family: "Figtree", sans-serif !important;
  padding: 0.45rem 1.15rem !important;
  box-shadow: 0 0 0 1px rgba(0, 237, 100, 0.2);
}

div.stButton > button:hover {
  filter: brightness(1.05);
}

div.stButton > button:disabled {
  background: #3D4F58 !important;
  color: #889397 !important;
}

.docs-placeholder {
  display: none;
}

.docs-heading {
  color: var(--mdb-green);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 0.72rem;
  margin: 1.4rem 0 0.55rem 0;
}

div[data-testid="stTabs"] {
  background: var(--mdb-card);
  border: 1px solid var(--mdb-border);
  border-radius: 14px;
  padding: 0.35rem 0.9rem 1.1rem 0.9rem;
  min-height: 480px;
}

div[data-testid="stTabs"] button[data-baseweb="tab"] {
  color: var(--mdb-muted) !important;
  font-weight: 600 !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--mdb-green) !important;
}

div[data-testid="stDialog"] div[role="dialog"] {
  background: var(--mdb-card) !important;
  border: 1px solid rgba(0, 237, 100, 0.25);
}

@keyframes pulse {
  0%, 100% { opacity: 0.55; }
  50% { opacity: 1; }
}

@media (max-width: 1100px) {
  .options-grid { grid-template-columns: 1fr; }
  .show-title { font-size: 1.7rem; }
  .answer-tile { min-height: 120px; }
  .answer-letter { font-size: 3.6rem; }
}
"""


def inject() -> str:
    return f"<style>{CSS}</style>"


def hero_html(question_index: int, question_count: int, api_ok: bool) -> str:
    status_class = "" if api_ok else " down"
    status_label = "API live" if api_ok else "API offline"
    return textwrap.dedent(f"""\
        <div class="hero">
          <div class="hero-brand">
            <p class="eyebrow">MongoDB Quiz</p>
            <h1 class="show-title">RAG Quiz Show</h1>
            <p class="show-sub">Four retrieval strategies. One question. Who gets it right?</p>
          </div>
          <div class="hero-meta">
            <span class="badge{status_class}"><span class="dot"></span>{html.escape(status_label)}</span>
            <span class="badge">Question {question_index + 1} / {question_count}</span>
          </div>
        </div>
        """)


def question_card_html(
    number: int,
    stem: str,
    options: dict[str, str],
    *,
    correct: str | None = None,
    revealed: bool = False,
) -> str:
    option_items = []
    for letter in ("A", "B", "C", "D"):
        text = options.get(letter, "")
        extra = " correct" if revealed and letter == correct else ""
        option_items.append(
            f'<div class="option{extra}">'
            f'<div class="option-letter">{letter}</div>'
            f'<div class="option-text">{html.escape(text)}</div>'
            "</div>"
        )
    return (
        '<div class="question-card">'
        f'<div class="q-kicker">Live question {number}</div>'
        f'<p class="q-stem">{html.escape(stem)}</p>'
        f'<div class="options-grid">{"".join(option_items)}</div>'
        "</div>"
    )


def score_strip_html(names: list[str], scores: list[int]) -> str:
    pills = []
    for name, score in zip(names, scores):
        pills.append(
            '<div class="score-pill">'
            f'<div class="label">{html.escape(name)}</div>'
            f'<div class="value">{score}</div>'
            "</div>"
        )
    return f'<div class="score-strip">{"".join(pills)}</div>'


def podium_html(
    name: str,
    caption: str,
    letter: str | None,
    state: str,
    error: str | None = None,
    input_tokens: int | None = None,
) -> str:
    if state == "waiting":
        content = "?"
    elif state == "error":
        content = "ERR"
    else:
        content = html.escape((letter or "—").upper())

    token_line = ""
    if input_tokens is not None:
        token_line = (
            f'<span class="token-count">Input token count: {input_tokens:,}</span>'
        )

    error_line = ""
    if error and state == "error":
        error_line = f'<p class="tile-error">{html.escape(error)}</p>'

    return (
        '<div class="podium-wrap">'
        '<div class="podium-head">'
        f'<p class="podium-name">{html.escape(name)}</p>'
        f'<p class="podium-caption">{html.escape(caption)}</p>'
        "</div>"
        f'<div class="answer-tile {html.escape(state)}">'
        f'<span class="answer-letter">{content}</span>'
        f"{token_line}"
        "</div>"
        f"{error_line}"
        "</div>"
    )


def podium_row_html(cells: list[str]) -> str:
    return f'<div class="podium-row">{"".join(cells)}</div>'


def end_card_html(winner_line: str) -> str:
    return (
        '<div class="end-card">'
        '<p class="eyebrow">That\'s a wrap</p>'
        "<h2>Show over</h2>"
        f"<p>{html.escape(winner_line)}</p>"
        "</div>"
    )
