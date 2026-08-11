from datetime import date, datetime, time
from uuid import UUID, uuid4
from sqlalchemy import Date, DateTime, ForeignKey, String, Time, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, Field
from src.services.chunking import ChunkingStrategy



class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    source: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    chunking_strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    chunk_count: Mapped[int] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    weaviate_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        nullable=False,
    )

    section: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )

    booking_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    booking_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )



class ChunkResponse(BaseModel):
    index: int
    text: str
    section: str | None = None


class DocumentIngestionResponse(BaseModel):
    document_id: UUID
    filename: str
    content_type: str | None
    chunking_strategy: ChunkingStrategy
    chunk_count: int
    chunks: list[ChunkResponse]


class DocumentIngestionError(BaseModel):
    detail: str

