import { useEffect, useState } from "react";
import { getAnalyticsOverview } from "../services/api.js";


function Analytics() {

  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  async function loadAnalytics() {

    try {

      setError("");

      const data = await getAnalyticsOverview();

      setAnalytics(data);

    } catch (error) {

      console.error(
        "Analytics error:",
        error
      );

      setError(
        error.message ||
        "Unable to load analytics."
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {

    loadAnalytics();

    // Refresh analytics automatically
    // every 10 seconds.

    const interval = setInterval(
      loadAnalytics,
      10000
    );

    return () => {
      clearInterval(interval);
    };

  }, []);


  if (loading) {

    return (
      <div className="analytics-page">

        <h1>Learning Analytics</h1>

        <div className="analytics-loading">
          Loading your learning statistics...
        </div>

      </div>
    );
  }


  if (error) {

    return (
      <div className="analytics-page">

        <h1>Learning Analytics</h1>

        <div className="analytics-error">
          <strong>Unable to load analytics</strong>

          <p>{error}</p>

          <button
            onClick={loadAnalytics}
            className="analytics-refresh-button"
          >
            Try Again
          </button>
        </div>

      </div>
    );
  }


  const summary = analytics?.summary || {};

  const topics =
    analytics?.topic_performance || [];

  const recentQuizzes =
    analytics?.recent_quizzes || [];

  const history =
    analytics?.performance_history || [];


  return (
    <div className="analytics-page">

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <div className="analytics-header">

        <div>

          <h1>Learning Analytics</h1>

          <p>
            Track your learning progress and
            identify areas for improvement.
          </p>

        </div>

        <button
          className="analytics-refresh-button"
          onClick={loadAnalytics}
        >
          ↻ Refresh
        </button>

      </div>


      {/* ================================================= */}
      {/* SUMMARY CARDS */}
      {/* ================================================= */}

      <div className="analytics-summary-grid">

        <div className="analytics-card">

          <span className="analytics-card-icon">
            📝
          </span>

          <div>
            <p>Total Quizzes</p>

            <h2>
              {summary.total_quizzes || 0}
            </h2>
          </div>

        </div>


        <div className="analytics-card">

          <span className="analytics-card-icon">
            ❓
          </span>

          <div>
            <p>Questions Attempted</p>

            <h2>
              {summary.total_attempts || 0}
            </h2>
          </div>

        </div>


        <div className="analytics-card">

          <span className="analytics-card-icon">
            🎯
          </span>

          <div>
            <p>Accuracy</p>

            <h2>
              {summary.accuracy || 0}%
            </h2>
          </div>

        </div>


        <div className="analytics-card">

          <span className="analytics-card-icon">
            🏆
          </span>

          <div>
            <p>Average Score</p>

            <h2>
              {summary.average_score || 0}%
            </h2>
          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* PERFORMANCE */}
      {/* ================================================= */}

      <div className="analytics-grid">

        <section className="analytics-panel">

          <div className="analytics-panel-header">

            <div>

              <h2>
                Performance Over Time
              </h2>

              <p>
                Your recent quiz performance
              </p>

            </div>

          </div>


          {history.length === 0 ? (

            <div className="analytics-empty">
              Complete a quiz to see your
              performance history.
            </div>

          ) : (

            <div className="performance-chart">

              {history.map((item) => (

                <div
                  className="performance-bar-wrapper"
                  key={item.quiz_id}
                >

                  <div
                    className="performance-bar"
                    style={{
                      height: `${Math.max(
                        item.percentage,
                        5
                      )}%`
                    }}
                  >
                    <span>
                      {item.percentage}%
                    </span>
                  </div>

                  <div className="performance-label">

                    Quiz {item.quiz_id}

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>


        {/* ================================================= */}
        {/* TOPIC PERFORMANCE */}
        {/* ================================================= */}

        <section className="analytics-panel">

          <div className="analytics-panel-header">

            <div>

              <h2>
                Topic Performance
              </h2>

              <p>
                Accuracy by topic
              </p>

            </div>

          </div>


          {topics.length === 0 ? (

            <div className="analytics-empty">
              Complete quiz questions to see
              topic-wise performance.
            </div>

          ) : (

            <div className="topic-list">

              {topics.map((topic) => (

                <div
                  className="topic-item"
                  key={topic.topic}
                >

                  <div className="topic-header">

                    <span>
                      {topic.topic}
                    </span>

                    <strong>
                      {topic.accuracy}%
                    </strong>

                  </div>

                  <div className="topic-progress">

                    <div
                      className="topic-progress-fill"
                      style={{
                        width: `${topic.accuracy}%`
                      }}
                    />

                  </div>

                  <div className="topic-details">

                    <span>
                      {topic.correct} correct
                    </span>

                    <span>
                      {topic.incorrect} incorrect
                    </span>

                    <span>
                      {topic.attempted} attempted
                    </span>

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>

      </div>


      {/* ================================================= */}
      {/* RECENT QUIZZES */}
      {/* ================================================= */}

      <section className="analytics-panel">

        <div className="analytics-panel-header">

          <div>

            <h2>
              Recent Quiz Results
            </h2>

            <p>
              Your latest completed quizzes
            </p>

          </div>

        </div>


        {recentQuizzes.length === 0 ? (

          <div className="analytics-empty">

            No completed quizzes yet.

          </div>

        ) : (

          <div className="quiz-results-table">

            <div className="quiz-table-header">

              <span>Quiz</span>
              <span>Difficulty</span>
              <span>Score</span>
              <span>Accuracy</span>

            </div>


            {recentQuizzes.map((quiz) => (

              <div
                className="quiz-table-row"
                key={quiz.quiz_id}
              >

                <span className="quiz-name">

                  {quiz.title}

                </span>


                <span className="quiz-difficulty">

                  {quiz.difficulty}

                </span>


                <span>

                  {quiz.correct_answers}/
                  {quiz.total_questions}

                </span>


                <span>

                  <strong
                    className={
                      quiz.percentage >= 80
                        ? "score-good"
                        : quiz.percentage >= 50
                        ? "score-average"
                        : "score-low"
                    }
                  >
                    {quiz.percentage}%
                  </strong>

                </span>

              </div>

            ))}

          </div>

        )}

      </section>


      {/* ================================================= */}
      {/* LEARNING INSIGHT */}
      {/* ================================================= */}

      <section className="analytics-insight">

        <div className="insight-icon">
          💡
        </div>

        <div>

          <h2>
            Learning Insight
          </h2>

          {topics.length > 0 ? (

            <p>

              Your strongest topic is{" "}

              <strong>
                {topics[0].topic}
              </strong>

              {" "}with an accuracy of{" "}

              <strong>
                {topics[0].accuracy}%
              </strong>
              .

              {topics.length > 1 && (
                <>
                  {" "}Keep practicing your
                  other topics to improve your
                  overall performance.
                </>
              )}

            </p>

          ) : (

            <p>
              Complete your first quiz to
              receive personalized learning
              insights.
            </p>

          )}

        </div>

      </section>

    </div>
  );
}


export default Analytics;