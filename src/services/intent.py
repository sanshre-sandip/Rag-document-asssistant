from enum import Enum

from src.services.llm import generate


class Intent(str, Enum):
    RAG = "rag"
    BOOKING = "booking"


INTENT_PROMPT = """You are an intent classifier for a company assistant.

Classify the user's message into exactly one of these intents:

- rag: questions asking for information about the company, its
  technology, architecture, products, processes, or documents.
- booking: requests to schedule, book, arrange, or change an interview.

Return ONLY one word:
rag
or
booking
"""


def detect_intent(message: str) -> Intent:
    message = message.strip()

    if not message:
        raise ValueError("Message cannot be empty.")

    response = generate(
        messages=[
            {
                "role": "system",
                "content": INTENT_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        temperature=0,
        max_tokens=10,
    )

    value = response.strip().lower()

    if value == Intent.RAG.value:
        return Intent.RAG

    if value == Intent.BOOKING.value:
        return Intent.BOOKING

    raise ValueError(
        f"LLM returned invalid intent: {response!r}"
    )