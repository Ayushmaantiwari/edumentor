import { useEffect, useState } from "react";
import {
  generateQuiz,
  submitQuiz,
  getDocuments,
} from "../services/api.js";


function Quiz() {
  // ============================================================
  // STATE
  // ============================================================

  const [documents, setDocuments] = useState([]);

  const [selectedDocumentId, setSelectedDocumentId] =
    useState("");

  const [questionCount, setQuestionCount] =
    useState(5);

  const [difficulty, setDifficulty] =
    useState("medium");

  const [quiz, setQuiz] =
    useState(null);

  const [currentQuestion, setCurrentQuestion] =
    useState(0);

  const [answers, setAnswers] =
    useState({});

  const [results, setResults] =
    useState(null);

  const [loadingDocuments, setLoadingDocuments] =
    useState(true);

  const [generating, setGenerating] =
    useState(false);

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] =
    useState("");

  const [questionStartTime, setQuestionStartTime] =
    useState(Date.now());

  // ============================================================
  // LOAD DOCUMENTS
  // ============================================================

  useEffect(() => {
    loadDocuments();
  }, []);

  async function loadDocuments() {
    try {
      setLoadingDocuments(true);
      setError("");

      const data = await getDocuments();

      const docs = data.documents || data || [];

      setDocuments(docs);

      if (docs.length > 0) {
        setSelectedDocumentId(String(docs[0].id));
      }

    } catch (err) {

      console.error("Failed to load documents:", err);

      setError(
        err.message ||
        "Failed to load your study materials."
      );

    } finally {

      setLoadingDocuments(false);

    }
  }

  // ============================================================
  // GENERATE QUIZ
  // ============================================================

  async function handleGenerateQuiz() {

    if (!selectedDocumentId) {

      setError(
        "Please select a study material first."
      );

      return;
    }

    try {

      setGenerating(true);
      setError("");
      setResults(null);
      setAnswers({});
      setCurrentQuestion(0);

      const data = await generateQuiz(
        selectedDocumentId,
        questionCount,
        difficulty
      );

      setQuiz(data);

      setQuestionStartTime(Date.now());

    } catch (err) {

      console.error("Quiz generation failed:", err);

      setError(
        err.message ||
        "Failed to generate the quiz."
      );

    } finally {

      setGenerating(false);

    }
  }

  // ============================================================
  // SELECT ANSWER
  // ============================================================

  function selectAnswer(option) {

    if (!quiz || results) {
      return;
    }

    const question =
      quiz.questions[currentQuestion];

    setAnswers((previous) => ({
      ...previous,
      [question.id]: option,
    }));
  }

  // ============================================================
  // NEXT QUESTION
  // ============================================================

  function goToNextQuestion() {

    if (!quiz) {
      return;
    }

    if (
      currentQuestion <
      quiz.questions.length - 1
    ) {

      setCurrentQuestion(
        currentQuestion + 1
      );

      setQuestionStartTime(Date.now());
    }
  }

  // ============================================================
  // PREVIOUS QUESTION
  // ============================================================

  function goToPreviousQuestion() {

    if (currentQuestion > 0) {

      setCurrentQuestion(
        currentQuestion - 1
      );

      setQuestionStartTime(Date.now());
    }
  }

  // ============================================================
  // SUBMIT QUIZ
  // ============================================================

  async function handleSubmitQuiz() {

    if (!quiz) {
      return;
    }

    const unanswered =
      quiz.questions.filter(
        (question) =>
          !answers[question.id]
      );

    if (unanswered.length > 0) {

      const shouldSubmit =
        window.confirm(
          `You have ${unanswered.length} unanswered question${
            unanswered.length > 1
              ? "s"
              : ""
          }. Do you want to submit anyway?`
        );

      if (!shouldSubmit) {
        return;
      }
    }

    try {

      setSubmitting(true);
      setError("");

      const submissionAnswers =
        quiz.questions.map(
          (question) => {

            let timeTaken = 0;

            if (
              question.id ===
              quiz.questions[currentQuestion].id
            ) {

              timeTaken = Math.max(
                0,
                Math.floor(
                  (Date.now() -
                    questionStartTime) /
                    1000
                )
              );
            }

            return {
              question_id:
                question.id,

              selected_answer:
                answers[question.id] ||
                "",

              time_taken:
                timeTaken,
            };
          }
        );

      const data = await submitQuiz(
        quiz.quiz_id,
        submissionAnswers
      );

      setResults(data);

    } catch (err) {

      console.error(
        "Quiz submission failed:",
        err
      );

      setError(
        err.message ||
        "Failed to submit quiz."
      );

    } finally {

      setSubmitting(false);

    }
  }

  // ============================================================
  // START NEW QUIZ
  // ============================================================

  function startNewQuiz() {

    setQuiz(null);
    setResults(null);
    setAnswers({});
    setCurrentQuestion(0);
    setError("");
    setQuestionStartTime(Date.now());
  }

  // ============================================================
  // GET SELECTED DOCUMENT
  // ============================================================

  const selectedDocument =
    documents.find(
      (document) =>
        String(document.id) ===
        String(selectedDocumentId)
    );

  // ============================================================
  // QUIZ SETUP SCREEN
  // ============================================================

  if (!quiz) {

    return (
      <div className="quiz-page">

        <div className="quiz-hero">

          <div className="quiz-hero-icon">
            ✦
          </div>

          <div>
            <span className="quiz-eyebrow">
              AI POWERED LEARNING
            </span>

            <h1>
              Test your knowledge
            </h1>

            <p>
              Generate an intelligent quiz from
              your study material and discover
              how well you understand it.
            </p>
          </div>

        </div>


        {error && (
          <div className="quiz-error">
            <span>⚠</span>
            <div>{error}</div>
          </div>
        )}


        <div className="quiz-setup-card">

          <div className="setup-header">

            <div>

              <h2>
                Create a new quiz
              </h2>

              <p>
                Choose your study material and
                customize your quiz.
              </p>

            </div>

            <div className="setup-badge">
              AI Quiz
            </div>

          </div>


          <div className="quiz-form-grid">

            {/* DOCUMENT */}

            <div className="quiz-form-group full-width">

              <label>
                <span className="label-icon">
                  📚
                </span>

                Study material
              </label>

              {loadingDocuments ? (

                <div className="quiz-select-loading">
                  Loading your documents...
                </div>

              ) : documents.length === 0 ? (

                <div className="quiz-no-documents">

                  <div className="empty-icon">
                    📄
                  </div>

                  <div>
                    <strong>
                      No study materials found
                    </strong>

                    <p>
                      Upload a PDF from the
                      Documents section first.
                    </p>
                  </div>

                </div>

              ) : (

                <select
                  value={selectedDocumentId}
                  onChange={(event) =>
                    setSelectedDocumentId(
                      event.target.value
                    )
                  }
                  className="quiz-select"
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

              {selectedDocument && (
                <div className="selected-file">

                  <span>✓</span>

                  <span>
                    {selectedDocument.filename}
                  </span>

                  <span className="file-ready">
                    Ready
                  </span>

                </div>
              )}

            </div>


            {/* QUESTION COUNT */}

            <div className="quiz-form-group">

              <label>
                <span className="label-icon">
                  🔢
                </span>

                Questions
              </label>

              <select
                value={questionCount}
                onChange={(event) =>
                  setQuestionCount(
                    Number(event.target.value)
                  )
                }
                className="quiz-select"
              >

                <option value={5}>
                  5 questions
                </option>

                <option value={10}>
                  10 questions
                </option>

                <option value={15}>
                  15 questions
                </option>

                <option value={20}>
                  20 questions
                </option>

              </select>

            </div>


            {/* DIFFICULTY */}

            <div className="quiz-form-group">

              <label>
                <span className="label-icon">
                  🎯
                </span>

                Difficulty
              </label>

              <select
                value={difficulty}
                onChange={(event) =>
                  setDifficulty(
                    event.target.value
                  )
                }
                className="quiz-select"
              >

                <option value="easy">
                  Easy
                </option>

                <option value="medium">
                  Medium
                </option>

                <option value="hard">
                  Hard
                </option>

              </select>

            </div>

          </div>


          {/* QUIZ FEATURES */}

          <div className="quiz-features">

            <div className="quiz-feature">

              <div className="feature-icon">
                ✨
              </div>

              <div>
                <strong>
                  AI Generated
                </strong>

                <span>
                  Questions based on your PDF
                </span>
              </div>

            </div>


            <div className="quiz-feature">

              <div className="feature-icon">
                🎯
              </div>

              <div>
                <strong>
                  Personalized
                </strong>

                <span>
                  Choose your difficulty
                </span>
              </div>

            </div>


            <div className="quiz-feature">

              <div className="feature-icon">
                💡
              </div>

              <div>
                <strong>
                  Smart Feedback
                </strong>

                <span>
                  Get explanations after submission
                </span>
              </div>

            </div>

          </div>


          <button
            className="generate-quiz-button"
            onClick={handleGenerateQuiz}
            disabled={
              generating ||
              loadingDocuments ||
              documents.length === 0
            }
          >

            {generating ? (

              <>
                <span className="button-spinner"></span>

                Generating your quiz...
              </>

            ) : (

              <>
                ✦ Generate Quiz
              </>

            )}

          </button>

        </div>

      </div>
    );
  }


  // ============================================================
  // RESULT SCREEN
  // ============================================================

  if (results) {

    const percentage =
      Number(results.percentage || 0);

    const score =
      results.correct_answers || 0;

    const total =
      results.total_questions || 0;

    let resultMessage =
      "Keep practicing!";

    if (percentage >= 90) {
      resultMessage =
        "Outstanding performance!";
    } else if (percentage >= 75) {
      resultMessage =
        "Great job! You're doing really well.";
    } else if (percentage >= 50) {
      resultMessage =
        "Good effort! Keep improving.";
    }

    return (
      <div className="quiz-page">

        <div className="result-card">

          <div className="result-trophy">
            {percentage >= 75
              ? "🏆"
              : "🎯"}
          </div>

          <span className="result-label">
            QUIZ COMPLETED
          </span>

          <h1>
            {resultMessage}
          </h1>

          <p className="result-subtitle">
            {quiz.document_name}
          </p>


          <div className="score-circle">

            <div className="score-inner">

              <strong>
                {percentage}%
              </strong>

              <span>
                Score
              </span>

            </div>

          </div>


          <div className="result-stats">

            <div className="result-stat">

              <span className="stat-icon">
                ✓
              </span>

              <strong>
                {score}
              </strong>

              <span>
                Correct
              </span>

            </div>


            <div className="result-stat">

              <span className="stat-icon incorrect">
                ×
              </span>

              <strong>
                {results.incorrect_answers}
              </strong>

              <span>
                Incorrect
              </span>

            </div>


            <div className="result-stat">

              <span className="stat-icon neutral">
                #
              </span>

              <strong>
                {total}
              </strong>

              <span>
                Questions
              </span>

            </div>

          </div>


          <div className="result-actions">

            <button
              className="primary-result-button"
              onClick={() => {
                setResults(null);
                setCurrentQuestion(0);
              }}
            >
              Review Answers
            </button>

            <button
              className="secondary-result-button"
              onClick={startNewQuiz}
            >
              Create Another Quiz
            </button>

          </div>

        </div>


        {/* REVIEW */}

        <div className="review-section">

          <div className="review-header">

            <div>

              <span className="quiz-eyebrow">
                PERFORMANCE REVIEW
              </span>

              <h2>
                Review your answers
              </h2>

            </div>

            <span className="review-score">
              {score}/{total}
            </span>

          </div>


          {results.results.map(
            (result, index) => {

              const question =
                quiz.questions.find(
                  (item) =>
                    item.id ===
                    result.question_id
                );

              if (!question) {
                return null;
              }

              const selectedText =
                question.options[
                  result.selected_answer
                ];

              const correctText =
                question.options[
                  result.correct_answer
                ];

              return (
                <div
                  key={result.question_id}
                  className={`review-card ${
                    result.is_correct
                      ? "review-correct"
                      : "review-incorrect"
                  }`}
                >

                  <div className="review-question-top">

                    <div className="review-number">
                      {String(index + 1).padStart(
                        2,
                        "0"
                      )}
                    </div>

                    <div className="review-status">

                      {result.is_correct
                        ? "✓ Correct"
                        : "× Incorrect"}

                    </div>

                  </div>


                  <h3>
                    {question.question}
                  </h3>


                  <div className="review-answer-row">

                    <div>
                      <span>
                        Your answer
                      </span>

                      <strong>
                        {result.selected_answer
                          ? `${result.selected_answer}. ${selectedText}`
                          : "Not answered"}
                      </strong>
                    </div>


                    {!result.is_correct && (
                      <div>

                        <span>
                          Correct answer
                        </span>

                        <strong className="correct-answer">
                          {result.correct_answer}.{" "}
                          {correctText}
                        </strong>

                      </div>
                    )}

                  </div>


                  <div className="explanation-box">

                    <span className="explanation-icon">
                      💡
                    </span>

                    <div>

                      <strong>
                        Explanation
                      </strong>

                      <p>
                        {result.explanation}
                      </p>

                    </div>

                  </div>

                </div>
              );
            }
          )}

        </div>

      </div>
    );
  }


  // ============================================================
  // ACTIVE QUIZ
  // ============================================================

  const question =
    quiz.questions[currentQuestion];

  const selectedAnswer =
    answers[question.id];

  const progress =
    ((currentQuestion + 1) /
      quiz.questions.length) *
    100;

  const isLastQuestion =
    currentQuestion ===
    quiz.questions.length - 1;


  return (
    <div className="quiz-page">

      {/* QUIZ HEADER */}

      <div className="active-quiz-header">

        <div>

          <button
            className="back-to-setup"
            onClick={startNewQuiz}
          >
            ← Exit quiz
          </button>

          <h1>
            {quiz.title}
          </h1>

          <p>
            {quiz.document_name}
          </p>

        </div>


        <div className="quiz-meta">

          <span className="difficulty-pill">
            {quiz.difficulty}
          </span>

          <span className="question-count-pill">
            {quiz.question_count} Questions
          </span>

        </div>

      </div>


      {/* PROGRESS */}

      <div className="quiz-progress-container">

        <div className="progress-info">

          <span>
            Question{" "}
            <strong>
              {currentQuestion + 1}
            </strong>{" "}
            of{" "}
            <strong>
              {quiz.questions.length}
            </strong>
          </span>

          <span>
            {Math.round(progress)}% complete
          </span>

        </div>

        <div className="quiz-progress-track">

          <div
            className="quiz-progress-bar"
            style={{
              width: `${progress}%`,
            }}
          />

        </div>

      </div>


      {/* MAIN QUIZ */}

      <div className="quiz-content">

        {/* QUESTION NAVIGATION */}

        <div className="question-navigation">

          <span className="navigation-title">
            Questions
          </span>

          <div className="question-dots">

            {quiz.questions.map(
              (item, index) => {

                const answered =
                  answers[item.id];

                return (
                  <button
                    key={item.id}
                    className={`question-dot ${
                      index === currentQuestion
                        ? "active"
                        : ""
                    } ${
                      answered
                        ? "answered"
                        : ""
                    }`}
                    onClick={() => {
                      setCurrentQuestion(index);
                      setQuestionStartTime(
                        Date.now()
                      );
                    }}
                  >
                    {index + 1}
                  </button>
                );
              }
            )}

          </div>

          <div className="navigation-legend">

            <span>
              <i className="legend-current"></i>
              Current
            </span>

            <span>
              <i className="legend-answered"></i>
              Answered
            </span>

          </div>

        </div>


        {/* QUESTION CARD */}

        <div className="question-card">

          <div className="question-card-top">

            <span className="question-label">
              QUESTION{" "}
              {String(
                currentQuestion + 1
              ).padStart(2, "0")}
            </span>

            <span className="question-type">
              Single choice
            </span>

          </div>


          <h2 className="question-text">
            {question.question}
          </h2>


          <div className="options-container">

            {Object.entries(
              question.options
            ).map(
              ([letter, text]) => {

                const isSelected =
                  selectedAnswer === letter;

                return (
                  <button
                    key={letter}
                    className={`quiz-option ${
                      isSelected
                        ? "selected"
                        : ""
                    }`}
                    onClick={() =>
                      selectAnswer(letter)
                    }
                  >

                    <span className="option-letter">
                      {letter}
                    </span>

                    <span className="option-text">
                      {text}
                    </span>

                    <span className="option-check">

                      {isSelected
                        ? "✓"
                        : ""}

                    </span>

                  </button>
                );
              }
            )}

          </div>


          <div className="question-footer">

            <button
              className="previous-button"
              onClick={goToPreviousQuestion}
              disabled={
                currentQuestion === 0
              }
            >
              ← Previous
            </button>


            <span className="answer-status">

              {selectedAnswer ? (
                <>
                  <span>✓</span>
                  Answer selected
                </>
              ) : (
                "Select an answer"
              )}

            </span>


            {isLastQuestion ? (

              <button
                className="submit-quiz-button"
                onClick={handleSubmitQuiz}
                disabled={submitting}
              >

                {submitting ? (
                  <>
                    <span className="button-spinner"></span>
                    Submitting...
                  </>
                ) : (
                  <>
                    Submit Quiz ✓
                  </>
                )}

              </button>

            ) : (

              <button
                className="next-button"
                onClick={goToNextQuestion}
              >
                Next Question →
              </button>

            )}

          </div>

        </div>

      </div>

    </div>
  );
}


export default Quiz;