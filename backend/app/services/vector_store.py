from sqlalchemy import text

from app.database import engine

EMBEDDING_DIMENSION = 384


# ======================================================
# ADD EMBEDDINGS TO SUPABASE PGVECTOR
# ======================================================

def add_embeddings_to_faiss(embeddings, chunk_ids):
    """
    Store embeddings directly in Supabase pgvector.

    The function name is kept as add_embeddings_to_faiss()
    so existing code does not need to change yet.
    """

    if embeddings is None:
        raise ValueError("Embeddings cannot be None.")

    if chunk_ids is None:
        raise ValueError("chunk_ids cannot be None.")

    if len(embeddings) != len(chunk_ids):
        raise ValueError(
            f"Number of embeddings ({len(embeddings)}) "
            f"does not match number of chunk IDs ({len(chunk_ids)})."
        )

    if len(embeddings) == 0:
        return {
            "added": 0,
            "total_vectors": 0
        }

    for embedding, chunk_id in zip(embeddings, chunk_ids):

        if len(embedding) != EMBEDDING_DIMENSION:
            raise ValueError(
                f"Embedding dimension is {len(embedding)}, "
                f"expected {EMBEDDING_DIMENSION}."
            )

        embedding_string = "[" + ",".join(
            str(float(value)) for value in embedding
        ) + "]"

        with engine.begin() as connection:

            connection.execute(
                text("""
                    UPDATE document_chunks
                    SET embedding = CAST(:embedding AS vector)
                    WHERE id = :chunk_id
                """),
                {
                    "embedding": embedding_string,
                    "chunk_id": int(chunk_id)
                }
            )

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM document_chunks
                WHERE embedding IS NOT NULL
            """)
        ).scalar()

    print(
        f"Added {len(embeddings)} embeddings to Supabase pgvector."
    )

    print(
        f"Total stored embeddings: {result}"
    )

    return {
        "added": len(embeddings),
        "total_vectors": result
    }


# ======================================================
# SEARCH SUPABASE PGVECTOR
# ======================================================

def search_faiss(
    query_embedding,
    top_k: int = 5
):
    """
    Search Supabase pgvector using cosine distance.

    The function name is kept as search_faiss()
    so existing code does not need to change yet.
    """

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    if len(query_embedding) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Query embedding dimension is "
            f"{len(query_embedding)}, expected "
            f"{EMBEDDING_DIMENSION}."
        )

    embedding_string = "[" + ",".join(
        str(float(value)) for value in query_embedding
    ) + "]"

    with engine.connect() as connection:

        rows = connection.execute(
            text("""
                SELECT
                    id,
                    embedding <=> CAST(:embedding AS vector) AS distance
                FROM document_chunks
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :top_k
            """),
            {
                "embedding": embedding_string,
                "top_k": int(top_k)
            }
        ).fetchall()

    results = []

    for row in rows:
        results.append({
            "chunk_id": int(row[0]),
            "distance": float(row[1])
        })

    return results


# ======================================================
# VECTOR STORE INFORMATION
# ======================================================

def get_vector_store_info():
    """
    Return information about the Supabase vector store.
    """

    with engine.connect() as connection:

        total_vectors = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM document_chunks
                WHERE embedding IS NOT NULL
            """)
        ).scalar()

        total_chunks = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM document_chunks
            """)
        ).scalar()

    return {
        "embedding_dimension": EMBEDDING_DIMENSION,
        "total_vectors": int(total_vectors),
        "total_chunks": int(total_chunks),
        "consistent": total_vectors <= total_chunks
    }