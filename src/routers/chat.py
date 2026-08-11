from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.services.booking import (
    extract_booking_details,
    get_missing_field,
)
from src.services.booking_service import create_booking
from src.services.intent import Intent, detect_intent
from src.services.memory import (
    add_message,
    get_history,
)
from src.services.rag import answer_question


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Conversational RAG"],
)


class ChatRequest(BaseModel):
    conversation_id: str = Field(
        ...,
        min_length=1,
        description="Conversation identifier",
    )

    message: str = Field(
        ...,
        min_length=1,
        description="User message",
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve",
    )


class ChatSource(BaseModel):
    document_id: str | None
    filename: str | None
    section: str | None
    chunk_index: int | None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]


def booking_response(
    missing_field: str,
    name: str | None = None,
) -> str:
    if missing_field == "name":
        return "Sure! What is your name?"

    if missing_field == "email":
        if name:
            return f"Thanks, {name}. What is your email?"

        return "What is your email?"

    if missing_field == "date":
        return "What date would you prefer for the interview?"

    if missing_field == "time":
        return "What time would you prefer for the interview?"

    return "Please provide your interview details."


def booking_conversation_active(
    history: list[dict[str, str]],
) -> bool:
    """
    Determine whether the conversation is already in
    the interview-booking flow.
    """

    booking_phrases = (
        "what is your name",
        "what's your name",
        "what is your email",
        "what's your email",
        "what date would you prefer",
        "what time would you prefer",
        "interview details",
        "booking has been",
        "booking is ready",
    )

    for message in history:
        if message.get("role") != "assistant":
            continue

        content = message.get("content", "").lower()

        if any(
            phrase in content
            for phrase in booking_phrases
        ):
            return True

    return False


@router.get("/health")
async def chat_health() -> dict[str, str]:
    return {
        "service": "conversational-rag",
        "status": "ok",
    }


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:

    try:
        history = get_history(
            request.conversation_id,
        )

        intent = detect_intent(
            request.message,
        )

        # Continue an existing booking conversation.
        if booking_conversation_active(history):
            intent = Intent.BOOKING

        if intent == Intent.BOOKING:

            details = extract_booking_details(
                message=request.message,
                history=history,
            )

            missing_field = get_missing_field(
                details,
            )

            if missing_field:

                answer = booking_response(
                    missing_field=missing_field,
                    name=details.name,
                )

                add_message(
                    request.conversation_id,
                    "user",
                    request.message,
                )

                add_message(
                    request.conversation_id,
                    "assistant",
                    answer,
                )

                return ChatResponse(
                    answer=answer,
                    sources=[],
                )

            booking = await create_booking(
                db=db,
                details=details,
            )

            answer = (
                f"Your interview has been booked successfully for "
                f"{booking.booking_date.strftime('%B %d, %Y')} at "
                f"{booking.booking_time.strftime('%I:%M %p')}."
            )

            add_message(
                request.conversation_id,
                "user",
                request.message,
            )

            add_message(
                request.conversation_id,
                "assistant",
                answer,
            )

            return ChatResponse(
                answer=answer,
                sources=[],
            )

        answer, chunks = answer_question(
            query=request.message,
            limit=request.limit,
        )

        add_message(
            request.conversation_id,
            "user",
            request.message,
        )

        add_message(
            request.conversation_id,
            "assistant",
            answer,
        )

        sources = [
            ChatSource(
                document_id=chunk.document_id,
                filename=chunk.filename,
                section=chunk.section,
                chunk_index=chunk.chunk_index,
            )
            for chunk in chunks
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to process chat request.",
        ) from exc
