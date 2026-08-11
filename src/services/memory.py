import json

import redis

from src.config import REDIS_URL

MAX_HISTORY = 10
KEY_PREFIX = "chat:history:"


def get_redis_client() -> redis.Redis:
    return redis.from_url(
        REDIS_URL,
        decode_responses=True,
    )


def _key(conversation_id: str) -> str:
    return f"{KEY_PREFIX}{conversation_id}"


def get_history(
    conversation_id: str,
) -> list[dict[str, str]]:
    client = get_redis_client()

    raw_messages = client.lrange(
        _key(conversation_id),
        0,
        -1,
    )

    return [
        json.loads(message)
        for message in raw_messages
    ]


def add_message(
    conversation_id: str,
    role: str,
    content: str,
) -> None:
    if role not in {"user", "assistant"}:
        raise ValueError(
            "role must be 'user' or 'assistant'."
        )

    client = get_redis_client()

    key = _key(conversation_id)

    message = json.dumps(
        {
            "role": role,
            "content": content,
        }
    )

    client.rpush(key, message)

    # Keep only the most recent messages.
    client.ltrim(
        key,
        -MAX_HISTORY,
        -1,
    )


def clear_history(
    conversation_id: str,
) -> None:
    client = get_redis_client()
    client.delete(_key(conversation_id))