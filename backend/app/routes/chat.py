from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.utils.auth import get_current_user
from app.services.rag import answer_question


router = APIRouter(
    prefix="/api/chat",
    tags=["AI Tutor"]
)


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


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    print(
        f"AI Tutor request from user "
        f"{current_user.id}"
    )

    print(
        f"Selected document ID: "
        f"{request.document_id}"
    )

    # --------------------------------------------------
    # Verify that the selected document belongs
    # to the logged-in user
    # --------------------------------------------------

    document = (
        db.query(Document)
        .filter(
            Document.id == request.document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Selected document was not found "
                "or does not belong to your account."
            )
        )

    print(
        f"Selected document: "
        f"{document.filename}"
    )

    # --------------------------------------------------
    # Run document-specific RAG
    # --------------------------------------------------

    result = answer_question(
        db=db,
        question=request.question,
        user_id=current_user.id,
        document_id=request.document_id,
        top_k=request.top_k
    )

    # --------------------------------------------------
    # Return response
    # --------------------------------------------------

    return {
        "question": request.question,
        "document_id": document.id,
        "document_name": document.filename,
        "answer": result["answer"],
        "sources": result["sources"]
    }