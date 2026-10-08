import { useEffect, useState } from "react";

import {
  getDocuments,
  askTutor
} from "../services/api.js";


function Tutor() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocumentId, setSelectedDocumentId] =
    useState("");

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const [loadingDocuments, setLoadingDocuments] =
    useState(true);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  // ==================================================
  // Load user's PDFs
  // ==================================================

  useEffect(() => {
    async function loadDocuments() {
      try {
        setLoadingDocuments(true);
        setError("");

        const data = await getDocuments();

        const userDocuments =
          data.documents || [];

        setDocuments(userDocuments);

        // Automatically select first PDF
        if (userDocuments.length > 0) {
          setSelectedDocumentId(
            String(userDocuments[0].id)
          );
        }

      } catch (err) {
        console.error(
          "Failed to load documents:",
          err
        );

        setError(
          err.message ||
          "Failed to load your documents."
        );

      } finally {
        setLoadingDocuments(false);
      }
    }

    loadDocuments();
  }, []);


  // ==================================================
  // Handle PDF change
  // ==================================================

  function handleDocumentChange(event) {
    const documentId =
      event.target.value;

    setSelectedDocumentId(
      documentId
    );

    // Clear previous answer
    setAnswer("");

    // Clear previous sources
    setSources([]);

    // Clear previous error
    setError("");
  }


  // ==================================================
  // Ask AI Tutor
  // ==================================================

  async function askQuestion() {

    // ----------------------------------------------
    // Check question
    // ----------------------------------------------

    if (!question.trim()) {
      return;
    }


    // ----------------------------------------------
    // Check selected document
    // ----------------------------------------------

    if (!selectedDocumentId) {
      setError(
        "Please select a PDF before asking a question."
      );

      return;
    }


    // ----------------------------------------------
    // Start loading
    // ----------------------------------------------

    setLoading(true);

    setError("");
    setAnswer("");
    setSources("");


    try {

      // --------------------------------------------
      // Call backend through api.js
      // --------------------------------------------

      const data = await askTutor(
        question.trim(),
        selectedDocumentId,
        5
      );


      // --------------------------------------------
      // Set AI answer
      // --------------------------------------------

      setAnswer(
        data.answer || ""
      );


      // --------------------------------------------
      // Set sources
      // --------------------------------------------

      setSources(
        Array.isArray(data.sources)
          ? data.sources
          : []
      );


      // --------------------------------------------
      // Clear question after successful request
      // --------------------------------------------

      setQuestion("");

    } catch (err) {

      console.error(
        "AI Tutor error:",
        err
      );

      setError(
        err.message ||
        "Failed to get an answer from EduMentor."
      );

    } finally {

      setLoading(false);
    }
  }


  // ==================================================
  // Enter key
  // ==================================================

  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askQuestion();
    }
  }


  // ==================================================
  // Selected document
  // ==================================================

  const selectedDocument =
    documents.find(
      (document) =>
        String(document.id) ===
        String(selectedDocumentId)
    );


  // ==================================================
  // UI
  // ==================================================

  return (
    <div className="tutor-page">

      {/* ==================================================
          PAGE HEADER
          ================================================== */}

      <div className="page-header">

        <div>

          <h1>
            AI Tutor
          </h1>

          <p>
            Ask questions about your uploaded
            study material.
          </p>

        </div>

      </div>


      <div className="tutor-container">


        {/* ==================================================
            PDF SELECTION
            ================================================== */}

        <div className="document-selector-card">

          <label htmlFor="document-select">
            Choose study material
          </label>


          {loadingDocuments ? (

            <div className="document-loading">
              Loading your PDFs...
            </div>

          ) : documents.length === 0 ? (

            <div className="document-empty">
              No PDFs uploaded yet.
            </div>

          ) : (

            <select
              id="document-select"
              value={selectedDocumentId}
              onChange={
                handleDocumentChange
              }
            >

              {documents.map(
                (document) => (

                  <option
                    key={document.id}
                    value={document.id}
                  >
                    {document.filename}
                  </option>

                )
              )}

            </select>

          )}

        </div>


        {/* ==================================================
            SELECTED PDF
            ================================================== */}

        {selectedDocument && (

          <div className="selected-document">

            📄 Answer based on:{" "}

            <strong>
              {selectedDocument.filename}
            </strong>

          </div>

        )}


        {/* ==================================================
            QUESTION INPUT
            ================================================== */}

        <div className="chat-input-card">

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            onKeyDown={handleKeyDown}
            placeholder={
              selectedDocument
                ? `Ask EduMentor about ${selectedDocument.filename}...`
                : "Select a PDF and ask EduMentor..."
            }
            rows={4}
            disabled={
              loadingDocuments ||
              documents.length === 0 ||
              loading
            }
          />


          <button
            onClick={askQuestion}
            disabled={
              loading ||
              !question.trim() ||
              !selectedDocumentId ||
              loadingDocuments
            }
          >

            {loading
              ? "Thinking..."
              : "Ask EduMentor"}

          </button>

        </div>


        {/* ==================================================
            ERROR
            ================================================== */}

        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        {/* ==================================================
            ANSWER
            ================================================== */}

        {answer && (

          <div className="answer-card">


            {/* ----------------------------------------------
                ANSWER HEADER
                ---------------------------------------------- */}

            <div className="answer-header">

              <div className="ai-avatar">
                🤖
              </div>

              <div>

                <h2>
                  EduMentor
                </h2>

                <span>
                  AI Teaching Assistant
                </span>

              </div>

            </div>


            {/* ----------------------------------------------
                SELECTED PDF
                ---------------------------------------------- */}

            {selectedDocument && (

              <div className="answer-document">

                📄 Answer based on:{" "}

                <strong>
                  {selectedDocument.filename}
                </strong>

              </div>

            )}


            {/* ----------------------------------------------
                AI ANSWER
                ---------------------------------------------- */}

            <div className="answer-content">
              {answer}
            </div>


            {/* ----------------------------------------------
                SOURCES
                ---------------------------------------------- */}

            {sources.length > 0 && (

              <div className="sources">

                <h3>
                  Sources
                </h3>


                {sources.map(
                  (source, index) => (

                    <div
                      className="source-item"
                      key={
                        source.chunk_id ||
                        index
                      }
                    >

                      📄 Page{" "}

                      {source.page_number ??
                        source.page ??
                        "N/A"}

                    </div>

                  )
                )}

              </div>

            )}

          </div>

        )}

      </div>

    </div>
  );
}


export default Tutor;