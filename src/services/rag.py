from src.services.llm import generate
from src.services.retriever import RetrievedChunk, retrieve


SYSTEM_PROMPT = """You are a helpful company assistant.

Answer the user's question using ONLY the provided context and conversation history.

Rules:

- Do not invent information.
- If the answer is not contained in the context or conversation history, say you don't know.
- Use conversation history to understand follow-up questions.
- Give a concise and useful answer.
- Do not mention the retrieval process.
"""


def build_context(
    chunks: list[RetrievedChunk],
) -> str:
    """Build the context passed to the LLM."""

    if not chunks:
        return "No relevant information was found."

    sections = []

    for chunk in chunks:
        section = chunk.section or "Unknown section"

        sections.append(
            f"""Document: {chunk.filename}
Section: {section}
Chunk: {chunk.chunk_index}

Content:
{chunk.text}
"""
        )

    return "\n---\n".join(sections)


def build_history(
    history: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Convert Redis conversation history into LLM messages."""

    messages: list[dict[str, str]] = []

    for message in history:
        role = message.get("role")
        content = message.get("content")

        if role not in {"user", "assistant"}:
            continue

        if not content:
            continue

        messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    return messages


def answer_question(
    query: str,
    limit: int = 5,
    history: list[dict[str, str]] | None = None,
) -> tuple[str, list[RetrievedChunk]]:
    """
    Retrieve relevant chunks and generate an answer
    using conversation history.
    """

    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    if history is None:
        history = []

    chunks = retrieve(
        query=query,
        limit=limit,
    )

    context = build_context(chunks)

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
    ]

    messages.extend(
        build_history(history)
    )

    messages.append(
        {
            "role": "user",
            "content": f"""Context:

{context}

Question:
{query}

Answer:""",
        }
    )

    answer = generate(
        messages=messages,
        temperature=0.2,
        max_tokens=512,
    )

    return answer, chunks