from app.services.embeddings import generate_embedding


text = "The CPU executes instructions using the fetch decode execute cycle."


embedding = generate_embedding(text)


print("Embedding generated successfully.")
print("Vector dimension:", len(embedding))
print("First 10 values:", embedding[:10])