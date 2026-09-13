from app.database import SessionLocal

from app.services.embeddings import (
    generate_embedding
)

from app.services.vector_store import (
    search_faiss
)

from app.services.retrieval import (
    retrieve_chunks
)


# ======================================================
# TEST QUESTION
# ======================================================

question = "What is PWM?"


print("\n========================================")
print("RETRIEVAL TEST")
print("========================================")

print(
    f"\nQuestion: {question}"
)


# ======================================================
# STEP 1: GENERATE QUESTION EMBEDDING
# ======================================================

print(
    "\nSTEP 1: Generating question embedding..."
)

query_embedding = generate_embedding(
    question
)

print(
    "Question embedding generated."
)


# ======================================================
# STEP 2: SEARCH FAISS
# ======================================================

print(
    "\nSTEP 2: Searching FAISS..."
)

faiss_results = search_faiss(
    query_embedding,
    top_k=5
)


print(
    f"FAISS returned "
    f"{len(faiss_results)} results."
)


for result in faiss_results:

    print(
        f"Chunk ID: {result['chunk_id']} "
        f"| Distance: {result['distance']:.4f}"
    )


# ======================================================
# STEP 3: EXTRACT CHUNK IDs
# ======================================================

chunk_ids = [
    result["chunk_id"]
    for result in faiss_results
]


print(
    "\nChunk IDs:"
)

print(
    chunk_ids
)


# ======================================================
# STEP 4: CONNECT TO POSTGRESQL
# ======================================================

print(
    "\nSTEP 3: Retrieving chunks from PostgreSQL..."
)

db = SessionLocal()


try:

    retrieved_chunks = retrieve_chunks(
        db,
        chunk_ids
    )


    print(
        f"Retrieved "
        f"{len(retrieved_chunks)} chunks."
    )


    # ==================================================
    # STEP 5: DISPLAY ACTUAL PDF CONTENT
    # ==================================================

    print(
        "\n========================================"
    )

    print(
        "RETRIEVED PDF CONTENT"
    )

    print(
        "========================================"
    )


    for number, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        print(
            f"\n--- RESULT {number} ---"
        )

        print(
            f"Chunk ID: "
            f"{chunk['chunk_id']}"
        )

        print(
            f"Document ID: "
            f"{chunk['document_id']}"
        )

        print(
            f"Page: "
            f"{chunk['page_number']}"
        )

        print(
            f"Chunk Index: "
            f"{chunk['chunk_index']}"
        )

        print(
            "\nContent:"
        )

        print(
            chunk["content"]
        )


finally:

    db.close()


print(
    "\n========================================"
)

print(
    "RETRIEVAL TEST COMPLETE"
)

print(
    "========================================\n"
)