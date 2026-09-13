import { useEffect, useState } from "react";
import { getDocuments } from "../services/api.js";

function Tutor() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocumentId, setSelectedDocumentId] = useState("");

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // --------------------------------------------------
  // Load user's PDFs
  // --------------------------------------------------

  useEffect(() => {
    async function loadDocuments() {
      try {
        setLoadingDocuments(true);
        setError("");

        const data = await getDocuments();

        const userDocuments = data.documents || [];

        setDocuments(userDocuments);

        // Automatically select first PDF
        if (userDocuments.length > 0) {
          setSelectedDocumentId(
            String(userDocuments[0].id)
          );
        }
      } catch (err) {
        console.error(err);

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

  // --------------------------------------------------
  // Handle PDF change
  // --------------------------------------------------

  function handleDocumentChange(event) {
    const documentId = event.target.value;

    setSelectedDocumentId(documentId);

    // Clear old conversation answer
    setAnswer("");
    setSources([]);
    setError("");
  }

  // --------------------------------------------------
  // Ask question
  // --------------------------------------------------

  async function askQuestion() {

    if (!question.trim()) {
      return;
    }

    if (!selectedDocumentId) {
      setError(
        "Please select a PDF before asking a question."
      );
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {

      const token =
        localStorage.getItem("access_token");

      const response = await fetch(
        "http://localhost:8000/api/chat/",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            question: question.trim(),

            document_id:
              Number(selectedDocumentId),

            top_k: 5,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Failed to get AI response."
        );
      }

      setAnswer(data.answer || "");

      setSources(
        data.sources || []
      );

    } catch (err) {

      console.error(err);

      setError(
        err.message ||
        "Something went wrong."
      );

    } finally {

      setLoading(false);
    }
  }

  // --------------------------------------------------
  // Enter key
  // --------------------------------------------------

  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askQuestion();
    }
  }

  // --------------------------------------------------
  // Selected document
  // --------------------------------------------------

  const selectedDocument =
    documents.find(
      (document) =>
        String(document.id) ===
        String(selectedDocumentId)
    );

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="tutor-page">

      <div className="page-header">

        <div>

          <h1>AI Tutor</h1>

          <p>
            Ask questions about your uploaded
            study material.
          </p>

        </div>

      </div>


      <div className="tutor-container">

        {/* PDF Selection */}

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
              onChange={handleDocumentChange}
            >

              {documents.map((document) => (

                <option
                  key={document.id}
                  value={document.id}
                >
                  {document.filename}
                </option>

              ))}

            </select>

          )}

        </div>


        {/* Selected PDF */}

        {selectedDocument && (

          <div className="selected-document">

            📄 Answer based on:

            <strong>
              {selectedDocument.filename}
            </strong>

          </div>

        )}


        {/* Question */}

        <div className="chat-input-card">

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
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
              documents.length === 0
            }
          />

          <button
            onClick={askQuestion}
            disabled={
              loading ||
              !question.trim() ||
              !selectedDocumentId
            }
          >

            {loading
              ? "Thinking..."
              : "Ask EduMentor"}

          </button>

        </div>


        {/* Error */}

        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        {/* Answer */}

        {answer && (

          <div className="answer-card">

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


            {/* Selected PDF */}

            {selectedDocument && (

              <div className="answer-document">

                📄 Answer based on:

                <strong>
                  {selectedDocument.filename}
                </strong>

              </div>

            )}


            {/* AI Answer */}

            <div className="answer-content">
              {answer}
            </div>


            {/* Sources */}

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
                      {source.page_number}

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