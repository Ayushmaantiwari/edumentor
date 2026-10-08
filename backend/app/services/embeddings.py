import os
import numpy as np

from google import genai


# ======================================================
# GEMINI EMBEDDING CONFIGURATION
# ======================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


MODEL_NAME = "gemini-embedding-001"

EMBEDDING_DIMENSION = 384


# ======================================================
# NORMALIZE EMBEDDING
# ======================================================

def normalize_embedding(
    values: list[float]
) -> list[float]:

    vector = np.asarray(
        values,
        dtype=np.float32
    )

    norm = np.linalg.norm(vector)

    if norm == 0:
        return vector.tolist()

    vector = vector / norm

    return vector.tolist()


# ======================================================
# GENERATE ONE EMBEDDING
# ======================================================

def generate_embedding(
    text: str
) -> list[float]:

    result = client.models.embed_content(
        model=MODEL_NAME,
        contents=text,
        config={
            "output_dimensionality": EMBEDDING_DIMENSION
        }
    )

    embedding = result.embeddings[0].values

    return normalize_embedding(
        embedding
    )


# ======================================================
# GENERATE MULTIPLE EMBEDDINGS
# ======================================================

def generate_embeddings(
    texts: list[str]
) -> list[list[float]]:

    if not texts:
        return []

    result = client.models.embed_content(
        model=MODEL_NAME,
        contents=texts,
        config={
            "output_dimensionality": EMBEDDING_DIMENSION
        }
    )

    embeddings = []

    for embedding in result.embeddings:

        normalized = normalize_embedding(
            embedding.values
        )

        embeddings.append(
            normalized
        )

    return embeddings