from datetime import date, time

from pydantic import BaseModel, EmailStr

from src.services.llm import generate


class BookingDetails(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    booking_date: date | None = None
    booking_time: time | None = None


BOOKING_EXTRACTION_PROMPT = """You extract interview booking details.

Extract these fields from the conversation:

- name
- email
- booking_date
- booking_time

Return ONLY valid JSON with exactly these keys:

{
    "name": null,
    "email": null,
    "booking_date": null,
    "booking_time": null
}

Rules:

- Use null when a field is not provided.
- booking_date must use YYYY-MM-DD.
- booking_time must use 24-hour HH:MM.
- Do not invent missing information.
- Preserve information from previous conversation messages.
- The current date is 2026-08-11.
- The timezone is Asia/Kathmandu.
"""


def build_booking_context(
    history: list[dict[str, str]],
    current_message: str,
) -> str:
    """Build conversation context for booking extraction."""

    messages = []

    for message in history:
        role = message.get("role")
        content = message.get("content")

        if role and content:
            messages.append(
                f"{role}: {content}"
            )

    messages.append(
        f"user: {current_message}"
    )

    return "\n".join(messages)


def extract_booking_details(
    message: str,
    history: list[dict[str, str]] | None = None,
) -> BookingDetails:
    """Extract booking details from the conversation."""

    message = message.strip()

    if not message:
        raise ValueError("Message cannot be empty.")

    history = history or []

    context = build_booking_context(
        history=history,
        current_message=message,
    )

    response = generate(
        messages=[
            {
                "role": "system",
                "content": BOOKING_EXTRACTION_PROMPT,
            },
            {
                "role": "user",
                "content": context,
            },
        ],
        temperature=0,
        max_tokens=200,
        json_mode=True,
    )

    try:
        return BookingDetails.model_validate_json(response)

    except Exception as exc:
        raise ValueError(
            "Failed to extract booking details."
        ) from exc


def get_missing_field(
    details: BookingDetails,
) -> str | None:

    if not details.name:
        return "name"

    if not details.email:
        return "email"

    if not details.booking_date:
        return "date"

    if not details.booking_time:
        return "time"

    return None


def booking_is_complete(
    details: BookingDetails,
) -> bool:
    return get_missing_field(details) is None