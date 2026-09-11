from __future__ import annotations

from dataclasses import dataclass

QUESTIONS: dict[int, dict] = {
    1: {
        "stem": (
            "Quale provider viene usato in MongoDB Search per la funzione di autoEmbed, "
            "ovvero per abilitare la generazione automatizzata di text embedding sui "
            "documenti nel database?"
        ),
        "options": {
            "A": "OpenAI",
            "B": "Voyage AI",
            "C": "Hugging Face",
            "D": "AWS Bedrock",
        },
        "correct": "B",
    },
    2: {
        "stem": (
            "Nella definizione di un indice di vectorSearch in MongoDB, quale valore "
            "indicare per il campo fields.quantization affinchè ciascuna dimensione "
            "occupi esattamente un byte di memoria?"
        ),
        "options": {
            "A": 'scalar',
            "B": 'binary',
            "C": 'int8',
            "D": 'uint8',
        },
        "correct": "A",
    },
    3: {
        "stem": (
            "In una pipeline di aggregation MongoDB, quale stage - attualmente in "
            "Public Preview - consente di invocare un reranker Voyage AI direttamente "
            "all'interno di una query?"
        ),
        "options": {
            "A": "$rankFusion",
            "B": "$voyage",
            "C": "$scoreFusion",
            "D": "$rerank",
        },
        "correct": "D",
    },
}


@dataclass(frozen=True)
class Question:
    number: int
    prompt: str
    stem: str
    options: dict[str, str]
    correct: str


def _prompt(stem: str, options: dict[str, str]) -> str:
    lines = [stem, "", "Opzioni:"]
    lines.extend(f"- {letter}) {options[letter]}" for letter in ("A", "B", "C", "D"))
    return "\n".join(lines)


def load_questions() -> list[Question]:
    return [
        Question(
            number=number,
            prompt=_prompt(entry["stem"], entry["options"]),
            stem=entry["stem"],
            options=entry["options"],
            correct=entry["correct"],
        )
        for number, entry in QUESTIONS.items()
    ]
