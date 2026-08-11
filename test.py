from src.services.memory import (
    add_message,
    clear_history,
    get_history,
)


conversation_id = "test-conversation"

clear_history(conversation_id)

add_message(
    conversation_id,
    "user",
    "What technologies does the company use?",
)

add_message(
    conversation_id,
    "assistant",
    "The company uses Python, FastAPI, PostgreSQL, Redis, and Weaviate.",
)

history = get_history(conversation_id)

print("History:")
for message in history:
    print(message)