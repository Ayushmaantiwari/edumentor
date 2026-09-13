import numpy as np
from sqlalchemy.orm import Session

from app.services.embeddings import (
    generate_embedding,
    generate_embeddings
)

from app.services.retrieval import retrieve_document_chunks
from app.services.llm import generate_response


def cosine_similarity(query_vector, document_vectors):
    """
    Calculate cosine similarity between one query vector
    and multiple document vectors.
    """

    query_vector = np.asarray(
        query_vector,
        dtype=np.float32
    )

    document_vectors = np.asarray(
        document_vectors,
        dtype=np.float32
    )

    query_norm = np.linalg.norm(query_vector)

    document_norms = np.linalg.norm(
        document_vectors,
        axis=1
    )

    denominator = (
        document_norms * query_norm
    )

    denominator = np.where(
        denominator == 0,
        1e-10,
        denominator
    )

    similarities = (
        np.dot(
            document_vectors,
            query_vector
        )
        / denominator
    )

    return similarities


def answer_question(
    db: Session,
    question: str,
    user_id: int,
    document_id: int,
    top_k: int = 5
):
    """
    Answer a question using ONLY the selected PDF.

    Important:
    This implementation does NOT depend on the global
    FAISS index for document-specific retrieval.

    It retrieves chunks belonging to the selected PDF
    directly from PostgreSQL and ranks them using
    embedding similarity.
    """

    # --------------------------------------------------
    # STEP 1: Retrieve chunks from selected PDF
    # --------------------------------------------------

    document_chunks = retrieve_document_chunks(
        db=db,
        document_id=document_id,
        user_id=user_id
    )

    if not document_chunks:
        return {
            "answer": (
                "The selected PDF does not contain any "
                "processed study material."
            ),
            "sources": []
        }

    print(
        f"Document {document_id}: "
        f"{len(document_chunks)} chunks found."
    )

    # --------------------------------------------------
    # STEP 2: Generate embedding for the question
    # --------------------------------------------------

    query_embedding = generate_embedding(question)

    # --------------------------------------------------
    # STEP 3: Generate embeddings for selected PDF chunks
    # --------------------------------------------------

    chunk_texts = [
        chunk["content"]
        for chunk in document_chunks
    ]

    chunk_embeddings = generate_embeddings(
        chunk_texts
    )

    print(
        f"Generated embeddings for "
        f"{len(chunk_embeddings)} chunks."
    )

    # --------------------------------------------------
    # STEP 4: Calculate similarity
    # --------------------------------------------------

    similarities = cosine_similarity(
        query_embedding,
        chunk_embeddings
    )

    # --------------------------------------------------
    # STEP 5: Rank chunks by relevance
    # --------------------------------------------------

    ranked_indices = np.argsort(
        similarities
    )[::-1]

    # Take the requested number of chunks
    selected_indices = ranked_indices[:top_k]

    selected_chunks = []

    for index in selected_indices:

        chunk = document_chunks[int(index)]

        chunk_copy = dict(chunk)

        chunk_copy["similarity"] = float(
            similarities[int(index)]
        )

        selected_chunks.append(
            chunk_copy
        )

    print(
        "Selected chunk similarities:",
        [
            round(
                chunk["similarity"],
                4
            )
            for chunk in selected_chunks
        ]
    )

    # --------------------------------------------------
    # STEP 6: Build context for LLM
    # --------------------------------------------------

    context_parts = []

    for chunk in selected_chunks:

        context_parts.append(
            f"""
Page: {chunk['page_number']}

{chunk['content']}
"""
        )

    context = "\n".join(context_parts)

    # --------------------------------------------------
    # STEP 7: System prompt
    # --------------------------------------------------

    system_prompt = """
You are EduMentor, an AI teaching assistant.

Your job is to answer the student's question using
ONLY the provided content from the selected PDF.

IMPORTANT RULES:

1. Use ONLY the provided selected PDF content.
2. Do not use information from other uploaded PDFs.
3. Do not invent information.
4. Explain concepts clearly for a student.
5. Use simple language where possible.
6. Give step-by-step explanations when useful.
7. Use examples when they help understanding.
8. If the provided PDF content does not contain
   enough information to answer the question,
   clearly say that the selected PDF does not
   contain enough information.
9. Do not pretend that information is present
   when it is not.
"""

    # --------------------------------------------------
    # STEP 8: User prompt
    # --------------------------------------------------

    user_prompt = f"""
Selected PDF study material
================================

{context}

================================

Student Question:
{question}

================================

Answer the student's question using ONLY
the selected PDF study material above.
"""

    # --------------------------------------------------
    # STEP 9: Generate answer
    # --------------------------------------------------

    answer = generate_response(
        prompt=user_prompt,
        system_prompt=system_prompt
    )

    # --------------------------------------------------
    # STEP 10: Prepare sources
    # --------------------------------------------------

    sources = []

    for chunk in selected_chunks:

        sources.append(
            {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "page_number": chunk["page_number"],
                "similarity": round(
                    chunk["similarity"],
                    4
                )
            }
        )

    # --------------------------------------------------
    # STEP 11: Return result
    # --------------------------------------------------

    return {
        "answer": answer,
        "sources": sources
    }