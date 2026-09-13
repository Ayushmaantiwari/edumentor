from app.services.embeddings import generate_embedding
from app.services.vector_store import search_faiss


# ======================================================
# TEST QUESTION
# ======================================================

question = "What is PWM?"


print(
    f"\nQuestion: {question}"
)


# ======================================================
# GENERATE QUESTION EMBEDDING
# ======================================================

query_embedding = generate_embedding(
    question
)


print(
    "Query embedding generated."
)


print(
    f"Embedding dimension: "
    f"{len(query_embedding)}"
)


# ======================================================
# SEARCH FAISS
# ======================================================

results = search_faiss(
    query_embedding,
    top_k=5
)


print(
    "\nFAISS search results:"
)


for result in results:

    print(
        f"Chunk ID: {result['chunk_id']} "
        f"| Distance: {result['distance']:.4f}"
    )