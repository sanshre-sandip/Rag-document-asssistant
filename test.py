from src.services.booking import extract_booking_details
from src.services.memory import (
    add_message,
    clear_history,
    get_history,
)


conversation_id = "booking-test-001"

clear_history(conversation_id)

add_message(
    conversation_id,
    "user",
    "I want to schedule an interview.",
)

add_message(
    conversation_id,
    "assistant",
    "Sure. What is your name?",
)

add_message(
    conversation_id,
    "user",
    "My name is Sandip.",
)

add_message(
    conversation_id,
    "assistant",
    "Thanks Sandip. What is your email?",
)

add_message(
    conversation_id,
    "user",
    "My email is sandip@example.com.",
)

history = get_history(conversation_id)

details = extract_booking_details(
    message="My email is sandip@example.com.",
    history=history,
)

print("Name:", details.name)
print("Email:", details.email)
print("Date:", details.booking_date)
print("Time:", details.booking_time)