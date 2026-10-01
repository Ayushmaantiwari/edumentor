import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User

from app.utils.auth import get_current_user

from app.services.pdf_processor import (
    extract_text_from_pdf,
    chunk_text
)

from app.services.embeddings import (
    generate_embeddings
)

from app.services.vector_store import (
    add_embeddings_to_faiss
)


# ======================================================
# ROUTER
# ======================================================

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


# ======================================================
# UPLOAD DIRECTORY
# ======================================================

UPLOAD_DIRECTORY = "uploads"


# ======================================================
# UPLOAD PDF
# ======================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------
    # 1. Check whether file exists
    # --------------------------------------------------

    if not file:

        raise HTTPException(
            status_code=400,
            detail="No file uploaded"
        )


    # --------------------------------------------------
    # 2. Check PDF extension
    # --------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )


    # --------------------------------------------------
    # 3. Create user-specific upload directory
    # --------------------------------------------------

    user_directory = os.path.join(
        UPLOAD_DIRECTORY,
        str(current_user.id)
    )

    os.makedirs(
        user_directory,
        exist_ok=True
    )


    # --------------------------------------------------
    # 4. Create unique filename
    # --------------------------------------------------

    unique_filename = (
        f"{uuid.uuid4()}_{file.filename}"
    )


    # --------------------------------------------------
    # 5. Create complete file path
    # --------------------------------------------------

    file_path = os.path.join(
        user_directory,
        unique_filename
    )


    # --------------------------------------------------
    # 6. Save PDF to disk
    # --------------------------------------------------

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(content)


    print(
        "\nPDF saved successfully."
    )


    # ==================================================
    # CREATE DOCUMENT DATABASE RECORD
    # ==================================================

    document = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path
    )


    db.add(
        document
    )

    db.commit()

    db.refresh(
        document
    )


    print(
        f"Document created. ID: {document.id}"
    )


    # ==================================================
    # PHASE 4 + PHASE 5
    #
    # PDF
    # ↓
    # Extract text
    # ↓
    # Create chunks
    # ↓
    # PostgreSQL
    # ↓
    # Generate embeddings
    # ↓
    # FAISS
    # ==================================================

    print(
        "\n========== PDF PROCESSING STARTED =========="
    )


    # --------------------------------------------------
    # STEP 1: Extract text
    # --------------------------------------------------

    print(
        "STEP 1: Extracting PDF text..."
    )


    pages = extract_text_from_pdf(
        file_path
    )


    print(
        f"STEP 1 COMPLETE: "
        f"{len(pages)} pages extracted."
    )


    # --------------------------------------------------
    # STEP 2: Create chunks
    # --------------------------------------------------

    print(
        "STEP 2: Creating document chunks..."
    )


    chunk_index = 0

    created_chunks = []


    for page in pages:

        page_number = page["page_number"]

        page_text = page["text"]


        # Skip empty pages
        if not page_text:

            continue


        chunks = chunk_text(
            page_text
        )


        for chunk in chunks:

            document_chunk = DocumentChunk(
                document_id=document.id,
                page_number=page_number,
                chunk_index=chunk_index,
                content=chunk
            )


            db.add(
                document_chunk
            )


            created_chunks.append(
                document_chunk
            )


            chunk_index += 1


    print(
        f"STEP 2 COMPLETE: "
        f"{len(created_chunks)} chunks created."
    )


    # --------------------------------------------------
    # Check if PDF contains readable text
    # --------------------------------------------------

    if not created_chunks:

        print(
            "ERROR: No readable text found in PDF."
        )


        # Delete database record
        db.delete(
            document
        )

        db.commit()


        # Delete physical PDF
        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )


        raise HTTPException(
            status_code=400,
            detail=(
                "No readable text was found in this PDF. "
                "Please upload a PDF containing selectable text."
            )
        )


    # --------------------------------------------------
    # STEP 3: Save chunks to PostgreSQL
    # --------------------------------------------------

    print(
        "STEP 3: Saving chunks to PostgreSQL..."
    )


    db.commit()


    print(
        "STEP 3 COMPLETE: Chunks saved."
    )


    # --------------------------------------------------
    # STEP 4: Get PostgreSQL chunk IDs
    # --------------------------------------------------

    print(
        "STEP 4: Getting chunk IDs..."
    )


    for document_chunk in created_chunks:

        db.refresh(
            document_chunk
        )


    # Get chunk text
    chunk_texts = [
        document_chunk.content
        for document_chunk in created_chunks
    ]


    # Get PostgreSQL IDs
    chunk_ids = [
        document_chunk.id
        for document_chunk in created_chunks
    ]


    print(
        f"STEP 4 COMPLETE: "
        f"{len(chunk_ids)} chunk IDs obtained."
    )


    # --------------------------------------------------
    # STEP 5: Generate embeddings
    # --------------------------------------------------

    print(
        "STEP 5: Generating embeddings..."
    )


    embeddings = generate_embeddings(
        chunk_texts
    )


    print(
        f"STEP 5 COMPLETE: "
        f"{len(embeddings)} embeddings generated."
    )


    # --------------------------------------------------
    # STEP 6: Add embeddings to FAISS
    # --------------------------------------------------

    print(
        "STEP 6: Adding embeddings to FAISS..."
    )

    add_embeddings_to_faiss(
        embeddings,
        chunk_ids
    )

    print(
        "STEP 6 COMPLETE: FAISS index saved."
    )


    # --------------------------------------------------
    # STEP 7: Save embeddings to document chunks
    # --------------------------------------------------

    print(
        "STEP 7: Saving embeddings to PostgreSQL..."
    )

    for document_chunk, embedding in zip(
        created_chunks,
        embeddings
    ):
        document_chunk.embedding = embedding

    db.commit()

    print(
        "STEP 7 COMPLETE: Embeddings saved."
    )


    print(
        "========== PDF PROCESSING COMPLETE ==========\n"
    )


    # ==================================================
    # RETURN RESPONSE
    # ==================================================

    return {

        "message":
            "PDF uploaded and processed successfully",

        "document": {

            "id":
                document.id,

            "filename":
                document.filename,

            "file_path":
                document.file_path,

            "uploaded_at":
                document.uploaded_at,

            "chunks_created":
                len(created_chunks),

            "embeddings_created":
                len(embeddings)

        }

    }

# ======================================================
# GET ALL DOCUMENTS
# ======================================================

@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    documents = (
        db.query(Document)
        .filter(
            Document.user_id ==
            current_user.id
        )
        .order_by(
            Document.uploaded_at.desc()
        )
        .all()
    )


    return {

        "documents": [

            {

                "id":
                    document.id,

                "filename":
                    document.filename,

                "file_path":
                    document.file_path,

                "uploaded_at":
                    document.uploaded_at

            }

            for document in documents

        ]

    }


# ======================================================
# DELETE DOCUMENT
# ======================================================

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------
    # 1. Find document belonging to current user
    # --------------------------------------------------

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    # --------------------------------------------------
    # 2. Check document exists
    # --------------------------------------------------

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # --------------------------------------------------
    # 3. Delete document chunks
    # --------------------------------------------------

    deleted_chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id == document.id
        )
        .delete(
            synchronize_session=False
        )
    )

    print(
        f"Deleted {deleted_chunks} document chunks."
    )

    # --------------------------------------------------
    # 4. Delete physical PDF
    # --------------------------------------------------

    if os.path.exists(
        document.file_path
    ):

        os.remove(
            document.file_path
        )

        print(
            "Physical PDF deleted."
        )

    # --------------------------------------------------
    # 5. Delete document record
    # --------------------------------------------------

    db.delete(
        document
    )

    db.commit()

    print(
        f"Document {document.id} deleted successfully."
    )

    # --------------------------------------------------
    # 6. Return response
    # --------------------------------------------------

    return {
        "message": "Document deleted successfully",
        "document_id": document_id,
        "chunks_deleted": deleted_chunks
    }


    # --------------------------------------------------
    # Check document exists
    # --------------------------------------------------

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    # --------------------------------------------------
    # Delete physical PDF
    # --------------------------------------------------

    if os.path.exists(
        document.file_path
    ):

        os.remove(
            document.file_path
        )


    # --------------------------------------------------
    # Delete database record
    # --------------------------------------------------

    db.delete(
        document
    )

    db.commit()


    return {

        "message":
            "Document deleted successfully"

    }