from huggingface_hub import InferenceClient

from app.config import HF_TOKEN

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

client = InferenceClient(api_key=HF_TOKEN)


def generate_embedding(text: str) -> list[float]:
    embedding = client.feature_extraction(
        text,
        model=MODEL_NAME,
        normalize=True
    )

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    embeddings = client.feature_extraction(
        texts,
        model=MODEL_NAME,
        normalize=True
    )

    return embeddings.tolist()