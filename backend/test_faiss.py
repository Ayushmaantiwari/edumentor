import numpy as np
import faiss


dimension = 384


index = faiss.IndexFlatIP(
    dimension
)


vectors = np.random.random(
    (3, dimension)
).astype("float32")


index.add(vectors)


query = np.random.random(
    (1, dimension)
).astype("float32")


scores, indices = index.search(
    query,
    2
)


print("FAISS test successful.")
print("Number of vectors:", index.ntotal)
print("Similar vector indices:", indices)
print("Similarity scores:", scores)