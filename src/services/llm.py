from openai import OpenAI

from src.config import groq_base_url, groq_api_key, model

api = groq_api_key
base_url = groq_base_url
groq_model = model

def get_llm_client() -> OpenAI:
    """
    Create an OpenAI-compatible client configured for Groq.
    """

    return OpenAI(
        api_key=api,
        base_url=base_url,
    )


def generate(
    messages: list[dict[str, str]],
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> str:
    """
    Generate a response using the configured Groq model.
    """

    if not messages:
        raise ValueError("messages cannot be empty.")

    client = get_llm_client()

    response = client.chat.completions.create(
        model=groq_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    message = response.choices[0].message

    if not message.content:
        raise RuntimeError("Groq returned an empty response.")

    return message.content.strip()