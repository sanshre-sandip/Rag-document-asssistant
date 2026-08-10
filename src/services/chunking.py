from dataclasses import dataclass
from enum import Enum
import re


class ChunkingStrategy(str, Enum):
    STRUCTURE_AWARE = "structure_aware"
    RECURSIVE = "recursive"


@dataclass(slots=True)
class Chunk:
    text: str
    index: int
    section: str | None = None


DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 150


def chunk_text(
    text: str,
    strategy: ChunkingStrategy,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Chunk]:

    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    if strategy == ChunkingStrategy.RECURSIVE:
        return recursive_chunk(
            text,
            chunk_size,
            chunk_overlap,
        )

    if strategy == ChunkingStrategy.STRUCTURE_AWARE:
        return structure_aware_chunk(
            text,
            chunk_size,
            chunk_overlap,
        )

    raise ValueError(
        f"Unsupported chunking strategy: {strategy}"
    )


def recursive_chunk(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Chunk]:

    pieces = _recursive_split(
        text=text.strip(),
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
        chunk_size=chunk_size,
    )

    pieces = _add_overlap(
        pieces,
        chunk_overlap,
        chunk_size,
    )

    return [
        Chunk(
            text=piece,
            index=index,
        )
        for index, piece in enumerate(pieces)
        if piece.strip()
    ]


def structure_aware_chunk(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Chunk]:

    sections = _split_into_sections(text)

    chunks: list[Chunk] = []

    for section_title, section_text in sections:

        section_chunks = recursive_chunk(
            section_text,
            chunk_size,
            chunk_overlap,
        )

        for section_chunk in section_chunks:

            chunks.append(
                Chunk(
                    text=section_chunk.text,
                    index=len(chunks),
                    section=section_title,
                )
            )

    return chunks


def _split_into_sections(
    text: str,
) -> list[tuple[str | None, str]]:
    """
    Split a document into sections.

    Supported heading styles:

    Introduction

    ## Architecture

    1. Architecture

    SYSTEM ARCHITECTURE
    """

    lines = text.splitlines()

    sections: list[tuple[str | None, str]] = []

    current_heading: str | None = None
    current_content: list[str] = []

    for index, line in enumerate(lines):

        stripped = line.strip()

        # Preserve blank lines inside content.
        if not stripped:
            current_content.append("")
            continue

        previous_blank = (
            index == 0
            or not lines[index - 1].strip()
        )

        next_blank = (
            index == len(lines) - 1
            or not lines[index + 1].strip()
        )

        heading = _extract_heading(
            line=stripped,
            previous_blank=previous_blank,
            next_blank=next_blank,
        )

        if heading is not None:

            content = "\n".join(
                current_content
            ).strip()

            if content:
                sections.append(
                    (
                        current_heading,
                        content,
                    )
                )

            current_heading = heading
            current_content = []

            continue

        current_content.append(stripped)

    # Add the final section.
    content = "\n".join(
        current_content
    ).strip()

    if content:
        sections.append(
            (
                current_heading,
                content,
            )
        )

    return sections


def _extract_heading(
    line: str,
    previous_blank: bool = False,
    next_blank: bool = False,
) -> str | None:
    """
    Detect a likely document heading.
    """

    line = line.strip()

    if not line:
        return None

    # -----------------------------------------
    # Markdown heading
    # -----------------------------------------

    markdown_match = re.match(
        r"^#{1,6}\s+(.+?)\s*$",
        line,
    )

    if markdown_match:
        return markdown_match.group(1).strip()

    # -----------------------------------------
    # Numbered heading
    # -----------------------------------------

    numbered_match = re.match(
        r"^\d+(?:\.\d+)*[\.)]?\s+(.+?)\s*$",
        line,
    )

    if numbered_match:
        return numbered_match.group(1).strip()

    # -----------------------------------------
    # ALL CAPS heading
    # -----------------------------------------

    words = line.split()

    if (
        1 <= len(words) <= 10
        and line.isupper()
        and len(line) <= 100
    ):
        return line

    # -----------------------------------------
    # Plain standalone heading
    # -----------------------------------------

    if (
        previous_blank
        and next_blank
        and 1 <= len(words) <= 8
        and len(line) <= 80
        and not line.endswith(
            (".", "?", "!", ":")
        )
    ):
        return line

    return None


def _recursive_split(
    text: str,
    separators: list[str],
    chunk_size: int,
) -> list[str]:

    if len(text) <= chunk_size:
        return [text.strip()]

    if not separators:
        return [
            text[start:start + chunk_size].strip()
            for start in range(
                0,
                len(text),
                chunk_size,
            )
            if text[start:start + chunk_size].strip()
        ]

    separator = separators[0]

    if separator == "":
        parts = list(text)
    else:
        parts = text.split(separator)

    if len(parts) == 1:
        return _recursive_split(
            text,
            separators[1:],
            chunk_size,
        )

    pieces: list[str] = []
    current = ""

    for part in parts:

        part = part.strip()

        if not part:
            continue

        if current:
            candidate = (
                f"{current}{separator}{part}"
            )
        else:
            candidate = part

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            pieces.append(
                current.strip()
            )

        if len(part) <= chunk_size:
            current = part
        else:
            nested = _recursive_split(
                part,
                separators[1:],
                chunk_size,
            )

            pieces.extend(nested)
            current = ""

    if current:
        pieces.append(
            current.strip()
        )

    return pieces


def _add_overlap(
    chunks: list[str],
    chunk_overlap: int,
    chunk_size: int,
) -> list[str]:

    if not chunks or chunk_overlap == 0:
        return chunks

    result = [chunks[0]]

    for index in range(1, len(chunks)):

        previous = chunks[index - 1]
        current = chunks[index]

        overlap = previous[-chunk_overlap:]

        # Move to a word boundary.
        if " " in overlap:
            overlap = overlap.split(" ", 1)[1]

        combined = (
            f"{overlap} {current}"
        ).strip()

        if len(combined) > chunk_size:

            combined = combined[:chunk_size]

            if " " in combined:
                combined = combined.rsplit(
                    " ",
                    1,
                )[0]

        result.append(combined)

    return result