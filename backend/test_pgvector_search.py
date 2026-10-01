from app.services.embeddings import generate_embedding
from app.services.vector_store import search_faiss


query = "Test chunk for pgvector"

embedding = generate_embedding(query)

results = search_faiss(
    embedding,
    top_k=1
)

print("Search results:")
print(results)