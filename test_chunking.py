from pathlib import Path

from src.services.chunking import (
    ChunkingStrategy,
    chunk_text,
)


text = Path("test_data/sample.txt").read_text()


print("\n=== STRUCTURE-AWARE ===\n")

chunks = chunk_text(
    text,
    ChunkingStrategy.STRUCTURE_AWARE,
    chunk_size=300,
    chunk_overlap=50,
)

for chunk in chunks:
    print(
        f"[{chunk.index}] "
        f"section={chunk.section!r}"
    )
    print(chunk.text)
    print("-" * 60)


print("\n=== RECURSIVE ===\n")

chunks = chunk_text(
    text,
    ChunkingStrategy.RECURSIVE,
    chunk_size=300,
    chunk_overlap=50,
)

for chunk in chunks:
    print(f"[{chunk.index}]")
    print(chunk.text)
    print("-" * 60)