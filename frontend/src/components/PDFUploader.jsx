import { useRef, useState } from "react";

import {
  uploadDocument,
  getDocuments,
} from "../services/api.js";


function PDFUploader({
  onUploadSuccess
}) {

  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] =
    useState(null);

  const [uploading, setUploading] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");


  // ======================================================
  // SELECT PDF
  // ======================================================

  function handleFileSelect(event) {

    const file =
      event.target.files[0];

    setMessage("");
    setError("");

    if (!file) {
      return;
    }


    // Check PDF

    if (
      file.type !== "application/pdf" &&
      !file.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {

      setError(
        "Only PDF files are allowed."
      );

      setSelectedFile(null);

      return;
    }


    // Optional size check
    // 20 MB maximum

    const maxSize =
      20 * 1024 * 1024;

    if (file.size > maxSize) {

      setError(
        "PDF size must be less than 20 MB."
      );

      setSelectedFile(null);

      return;
    }


    setSelectedFile(file);

  }


  // ======================================================
  // CHECK WHETHER UPLOAD APPEARED
  // ======================================================

  async function findUploadedDocument(
    filename
  ) {

    const maxAttempts = 10;

    const delay = 2000;


    for (
      let attempt = 1;
      attempt <= maxAttempts;
      attempt++
    ) {

      try {

        const data =
          await getDocuments();

        const documents =
          data.documents || [];


        const uploadedDocument =
          documents.find(
            (document) =>
              document.filename === filename
          );


        if (uploadedDocument) {

          return uploadedDocument;

        }

      } catch (error) {

        console.log(
          "Waiting for document...",
          error
        );

      }


      if (
        attempt < maxAttempts
      ) {

        await new Promise(
          (resolve) =>
            setTimeout(
              resolve,
              delay
            )
        );

      }

    }


    return null;

  }


  // ======================================================
  // UPLOAD PDF
  // ======================================================

  async function handleUpload() {

    if (!selectedFile) {

      setError(
        "Please select a PDF first."
      );

      return;
    }


    setUploading(true);

    setMessage(
      "Uploading and processing your PDF..."
    );

    setError("");


    const filename =
      selectedFile.name;


    try {

      // --------------------------------------------------
      // Send PDF to backend
      // --------------------------------------------------

      const data =
        await uploadDocument(
          selectedFile
        );


      console.log(
        "Upload response:",
        data
      );


      // --------------------------------------------------
      // Backend successfully responded
      // --------------------------------------------------

      setMessage(
        data.message ||
        "PDF uploaded and processed successfully."
      );


      setSelectedFile(null);


      if (fileInputRef.current) {

        fileInputRef.current.value =
          "";

      }


      // --------------------------------------------------
      // Tell Documents page about new document
      // --------------------------------------------------

      if (onUploadSuccess) {

        try {

          await onUploadSuccess(
            data.document
          );

        } catch (callbackError) {

          /*
           * The PDF itself was successfully uploaded.
           *
           * A failure while refreshing the UI should
           * NOT make us show "upload failed".
           */

          console.error(
            "Document list refresh failed:",
            callbackError
          );

        }

      }

    } catch (error) {

      console.error(
        "Upload error:",
        error
      );


      // --------------------------------------------------
      // Possible connection interruption
      // --------------------------------------------------

      if (
        error.message ===
        "Failed to fetch"
      ) {

        setMessage(
          "Upload request was interrupted. Checking whether the PDF was saved..."
        );

        setError("");


        // ------------------------------------------------
        // The backend may have completed the upload
        // before the connection was interrupted.
        // ------------------------------------------------

        const uploadedDocument =
          await findUploadedDocument(
            filename
          );


        if (uploadedDocument) {

          setMessage(
            "PDF uploaded and processed successfully."
          );


          setSelectedFile(null);


          if (fileInputRef.current) {

            fileInputRef.current.value =
              "";

          }


          if (onUploadSuccess) {

            try {

              await onUploadSuccess(
                uploadedDocument
              );

            } catch (callbackError) {

              console.error(
                "Document refresh failed:",
                callbackError
              );

            }

          }

        } else {

          setMessage("");

          setError(
            "The upload connection was interrupted and the document could not be confirmed. Please try again."
          );

        }

      } else {

        setMessage("");

        setError(
          error.message ||
          "Failed to upload PDF."
        );

      }

    } finally {

      setUploading(false);

    }

  }


  // ======================================================
  // UI
  // ======================================================

  return (

    <div className="pdf-uploader">

      <div className="pdf-upload-area">


        {/* PDF ICON */}

        <div className="pdf-upload-icon">
          📄
        </div>


        {/* TITLE */}

        <h3>
          Upload a PDF
        </h3>


        <p>
          Select a PDF document to add it to EduMentor.
        </p>


        {/* FILE INPUT */}

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={
            handleFileSelect
          }
          hidden
        />


        {/* CHOOSE PDF */}

        <button
          type="button"
          className="upload-select-button"
          onClick={() =>
            fileInputRef.current?.click()
          }
          disabled={uploading}
        >

          Choose PDF

        </button>


        {/* SELECTED PDF */}

        {selectedFile && (

          <div className="selected-pdf">

            <span>
              📄
            </span>


            <div>

              <strong>
                {selectedFile.name}
              </strong>


              <small>

                {(
                  selectedFile.size /
                  (1024 * 1024)
                ).toFixed(2)} MB

              </small>

            </div>

          </div>

        )}


        {/* UPLOAD BUTTON */}

        {selectedFile && (

          <button
            type="button"
            className="upload-button"
            onClick={
              handleUpload
            }
            disabled={uploading}
          >

            {uploading
              ? "Processing PDF..."
              : "Upload PDF"}

          </button>

        )}


        {/* PROCESSING */}

        {uploading && (

          <div className="upload-processing">

            ⏳

            <span>
              Extracting text, creating embeddings
              and indexing your PDF...
            </span>

          </div>

        )}


        {/* SUCCESS */}

        {message && !error && (

          <div className="upload-success">

            ✓ {message}

          </div>

        )}


        {/* ERROR */}

        {error && (

          <div className="upload-error">

            ✕ {error}

          </div>

        )}

      </div>

    </div>

  );

}


export default PDFUploader;