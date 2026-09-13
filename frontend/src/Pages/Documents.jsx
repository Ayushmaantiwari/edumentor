import { useEffect, useState } from "react";

import PDFUploader from "../components/PDFUploader.jsx";

import {
  getDocuments,
  deleteDocument,
} from "../services/api.js";


function Documents() {

  const [documents, setDocuments] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  async function loadDocuments() {

    setLoading(true);

    setError("");


    try {

      const data = await getDocuments();

      setDocuments(
        data.documents || []
      );

    } catch (error) {

      setError(
        error.message ||
        "Failed to load documents."
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {

    loadDocuments();

  }, []);


  async function handleUploadSuccess(document) {

    /*
     * The backend has finished processing the PDF.
     *
     * Reload the document list so the new document
     * appears immediately without manually refreshing
     * the browser.
     */

    await loadDocuments();

  }


  async function handleDelete(documentId) {

    const confirmed = window.confirm(
      "Are you sure you want to delete this document?"
    );


    if (!confirmed) {
      return;
    }


    try {

      await deleteDocument(
        documentId
      );


      setDocuments(
        (currentDocuments) =>
          currentDocuments.filter(
            (document) =>
              document.id !== documentId
          )
      );

    } catch (error) {

      setError(
        error.message ||
        "Failed to delete document."
      );

    }

  }


  return (

    <div className="documents-page">

      <div className="page-header">

        <div>

          <h1>
            My Documents
          </h1>

          <p>
            Upload and manage your learning materials.
          </p>

        </div>

      </div>


      {/* PDF UPLOAD */}

      <PDFUploader
        onUploadSuccess={
          handleUploadSuccess
        }
      />


      {/* ERROR */}

      {error && (

        <div className="documents-error">

          {error}

        </div>

      )}


      {/* DOCUMENT SECTION */}

      <div className="documents-section">

        <div className="documents-section-header">

          <h2>
            Your Documents
          </h2>

          <span>

            {documents.length} document
            {documents.length !== 1
              ? "s"
              : ""}

          </span>

        </div>


        {/* LOADING */}

        {loading ? (

          <div className="documents-empty">

            Loading documents...

          </div>


        ) : documents.length === 0 ? (

          /* EMPTY */

          <div className="documents-empty">

            <div className="documents-empty-icon">
              📄
            </div>

            <h3>
              No documents yet
            </h3>

            <p>
              Upload your first PDF to get started.
            </p>

          </div>


        ) : (

          /* DOCUMENT LIST */

          <div className="documents-grid">

            {documents.map(
              (document) => (

                <div
                  className="document-card"
                  key={document.id}
                >

                  <div className="document-icon">
                    📄
                  </div>


                  <div className="document-info">

                    <h3>
                      {document.filename}
                    </h3>

                    <p>

                      Uploaded{" "}

                      {document.uploaded_at
                        ? new Date(
                            document.uploaded_at
                          ).toLocaleDateString()
                        : ""}

                    </p>

                  </div>


                  <button
                    className="document-delete"
                    onClick={() =>
                      handleDelete(
                        document.id
                      )
                    }
                    title="Delete document"
                  >

                    🗑️

                  </button>

                </div>

              )
            )}

          </div>

        )}

      </div>

    </div>

  );
}


export default Documents;