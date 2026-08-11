from src.services.llm import generate


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant.",
    },
    {
        "role": "user",
        "content": "Explain what FastAPI is in one sentence.",
    },
]


response = generate(
    messages=messages,
    temperature=0.2,
    max_tokens=100,
)

print("LLM response:")
print(response)
