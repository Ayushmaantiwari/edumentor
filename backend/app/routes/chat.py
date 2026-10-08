from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.utils.auth import get_current_user
from app.services.rag import answer_question


# ======================================================
# ROUTER
# ======================================================

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


# ======================================================
# REQUEST MODEL
# ======================================================

class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Student's question"
    )

    document_id: int = Field(
        ...,
        description="ID of the selected PDF document"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of relevant chunks"
    )


# ======================================================
# CHAT ENDPOINT
# ======================================================

@router.post("")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    print(
        "=========================================="
    )

    print(
        "AI TUTOR REQUEST"
    )

    print(
        f"User ID: {current_user.id}"
    )

    print(
        f"Document ID: {request.document_id}"
    )

    print(
        f"Question: {request.question}"
    )

    print(
        f"Top K: {request.top_k}"
    )

    print(
        "=========================================="
    )


    # ==================================================
    # STEP 1: VERIFY DOCUMENT
    # ==================================================

    try:

        document = (
            db.query(Document)
            .filter(
                Document.id == request.document_id,
                Document.user_id == current_user.id
            )
            .first()
        )

    except Exception as error:

        print(
            "========== DATABASE ERROR =========="
        )

        print(
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to verify the selected document."
            )
        )


    # ==================================================
    # STEP 2: DOCUMENT NOT FOUND
    # ==================================================

    if document is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Selected document was not found "
                "or does not belong to your account."
            )
        )


    print(
        f"Selected document: {document.filename}"
    )


    # ==================================================
    # STEP 3: RUN RAG
    # ==================================================

    try:

        print(
            "Starting document-specific RAG..."
        )

        result = answer_question(
            db=db,
            question=request.question,
            user_id=current_user.id,
            document_id=request.document_id,
            top_k=request.top_k
        )

        print(
            "RAG completed successfully."
        )


    except HTTPException:

        raise


    except Exception as error:

        print(
            "=========================================="
        )

        print(
            "CHAT / RAG ERROR"
        )

        print(
            f"Error type: {type(error).__name__}"
        )

        print(
            f"Error message: {str(error)}"
        )

        print(
            repr(error)
        )

        print(
            "=========================================="
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Chat generation failed: "
                f"{str(error)}"
            )
        )


    # ==================================================
    # STEP 4: VALIDATE RAG RESULT
    # ==================================================

    if not isinstance(result, dict):

        print(
            "Invalid RAG response:"
        )

        print(
            repr(result)
        )

        raise HTTPException(
            status_code=500,
            detail="Invalid response received from RAG service."
        )


    answer = result.get(
        "answer",
        ""
    )

    sources = result.get(
        "sources",
        []
    )


    # ==================================================
    # STEP 5: RETURN RESPONSE
    # ==================================================

    print(
        "Returning AI Tutor response."
    )

    print(
        f"Sources returned: {len(sources)}"
    )


    return {
        "question": request.question,

        "document_id": document.id,

        "document_name": document.filename,

        "answer": answer,

        "sources": sources
    }