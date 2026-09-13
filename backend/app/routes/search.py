from fastapi import APIRouter
from fastapi import Depends

from pydantic import BaseModel
from pydantic import Field

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User

from app.utils.auth import get_current_user

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
# ROUTER
# ======================================================

router = APIRouter(
    prefix="/api/search",
    tags=[
        "Semantic Search"
    ]
)


# ======================================================
# REQUEST MODEL
# ======================================================

class SearchRequest(BaseModel):

    query: str = Field(
        ...,
        min_length=1,
        description="Question or search query"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of relevant chunks"
    )


# ======================================================
# SEMANTIC SEARCH
# ======================================================

@router.post("/")
def semantic_search(

    request: SearchRequest,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    print(
        f"Authenticated user: "
        f"{current_user.id} - "
        f"{current_user.email}"
    )


    # ==================================================
    # STEP 1
    # Generate embedding for query
    # ==================================================

    print(
        "STEP 1: Generating query embedding..."
    )

    query_embedding = generate_embedding(
        request.query
    )


    # ==================================================
    # STEP 2
    # Search FAISS
    # ==================================================

    print(
        "STEP 2: Searching FAISS..."
    )

    faiss_results = search_faiss(
        query_embedding,
        top_k=request.top_k
    )


    # ==================================================
    # STEP 3
    # Extract chunk IDs
    # ==================================================

    chunk_ids = [
        result["chunk_id"]
        for result in faiss_results
    ]


    print(
        f"STEP 3: Found "
        f"{len(chunk_ids)} relevant chunks."
    )


    # ==================================================
    # STEP 4
    # Retrieve chunks from PostgreSQL
    # ==================================================

    print(
        "STEP 4: Retrieving chunks from PostgreSQL..."
    )

    retrieved_chunks = retrieve_chunks(
        db,
        chunk_ids,
        current_user.id
    )


    # ==================================================
    # STEP 5
    # Return results
    # ==================================================

    print(
        "STEP 5: Search completed."
    )


    return {

        "query": request.query,

        "results": retrieved_chunks

    }