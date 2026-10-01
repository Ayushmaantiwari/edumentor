from sqlalchemy import text

from app.database import engine
from app.services.embeddings import generate_embedding
from app.services.vector_store import add_embeddings_to_faiss


# --------------------------------------------------
# 1. Create a temporary user
# --------------------------------------------------

with engine.begin() as connection:
    result = connection.execute(
        text("""
            INSERT INTO users
            (name, email, password_hash)
            VALUES
            ('PGVector Test', 'pgvector_test@example.com', 'test')
            RETURNING id
        """)
    )

    user_id = result.scalar()

print("User ID:", user_id)


# --------------------------------------------------
# 2. Create a temporary document
# --------------------------------------------------

with engine.begin() as connection:
    result = connection.execute(
        text("""
            INSERT INTO documents
            (user_id, filename, file_path)
            VALUES
            (:user_id, 'pgvector_test.pdf', 'test/pgvector_test.pdf')
            RETURNING id
        """),
        {
            "user_id": user_id
        }
    )

    document_id = result.scalar()

print("Document ID:", document_id)


# --------------------------------------------------
# 3. Create a test chunk
# --------------------------------------------------

with engine.begin() as connection:
    result = connection.execute(
        text("""
            INSERT INTO document_chunks
            (document_id, page_number, chunk_index, content)
            VALUES
            (:document_id, 1, 0, 'Test chunk for pgvector')
            RETURNING id
        """),
        {
            "document_id": document_id
        }
    )

    chunk_id = result.scalar()

print("Chunk ID:", chunk_id)


# --------------------------------------------------
# 4. Generate embedding
# --------------------------------------------------

embedding = generate_embedding(
    "Test chunk for pgvector"
)

print(
    "Embedding dimensions:",
    len(embedding)
)


# --------------------------------------------------
# 5. Store embedding in Supabase pgvector
# --------------------------------------------------

result = add_embeddings_to_faiss(
    [embedding],
    [chunk_id]
)

print("Result:", result)