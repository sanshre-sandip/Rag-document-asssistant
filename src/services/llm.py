from openai import OpenAI

from src.config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL


def get_llm_client() -> OpenAI:
    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
    )


def generate(
    messages: list[dict[str, str]],
    temperature: float = 0.2,
    max_tokens: int = 512,
    json_mode: bool = False,
) -> str:
    """
    Generate a response using the configured Groq model.
    """

    if not messages:
        raise ValueError("messages cannot be empty.")

    client = get_llm_client()

    kwargs = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)

    message = response.choices[0].message

    if not message.content:
        raise RuntimeError("Groq returned an empty response.")

    return message.content.strip()