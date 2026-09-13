from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def retrieve_chunks(
    db: Session,
    chunk_ids: list[int],
    user_id: int
):
    """
    Retrieve specific document chunks belonging to the
    currently authenticated user.
    """

    if not chunk_ids:
        return []

    chunks = (
        db.query(DocumentChunk)
        .join(
            Document,
            DocumentChunk.document_id == Document.id
        )
        .filter(
            DocumentChunk.id.in_(chunk_ids),
            Document.user_id == user_id
        )
        .all()
    )

    chunk_lookup = {
        chunk.id: chunk
        for chunk in chunks
    }

    results = []

    for chunk_id in chunk_ids:
        chunk = chunk_lookup.get(chunk_id)

        if chunk is None:
            continue

        results.append(
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content
            }
        )

    return results


def retrieve_document_chunks(
    db: Session,
    document_id: int,
    user_id: int
):
    """
    Retrieve ALL chunks belonging to one selected document.

    This is intentionally document-specific and does not
    depend on the global FAISS index.
    """

    chunks = (
        db.query(DocumentChunk)
        .join(
            Document,
            DocumentChunk.document_id == Document.id
        )
        .filter(
            DocumentChunk.document_id == document_id,
            Document.user_id == user_id
        )
        .order_by(
            DocumentChunk.chunk_index.asc()
        )
        .all()
    )

    results = []

    for chunk in chunks:
        results.append(
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content
            }
        )

    return results