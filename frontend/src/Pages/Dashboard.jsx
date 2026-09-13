import { useEffect, useState } from "react";
import { testBackend } from "../services/api.js";
function Dashboard() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  useEffect(() => {
  async function checkBackend() {

    try {

      const data = await testBackend();

      if (data.status === "healthy") {
        setBackendStatus("Connected");
      } else {
        setBackendStatus("Disconnected");
      }

    } catch (error) {

      setBackendStatus("Disconnected");

    }

  }

  checkBackend();

}, []);
  return (
    <div className="dashboard">

      <div className="dashboard-body">

        {/* Main Content */}
        <main className="dashboard-main">

          {/* Welcome Section */}
          <section className="welcome-section">
            <div>
              <h1>Welcome back, Ayushmaan 👋</h1>
            <div className="backend-status">
            <span
              className={
                backendStatus === "Connected"
                  ? "status-dot connected"
                  : "status-dot disconnected"
              }
            ></span>

            <span>
              Backend: {backendStatus}
            </span>
          </div>

              <p>
                Continue learning, practice your concepts,
                and improve your knowledge with EduMentor.
              </p>
            </div>

            <div className="study-date">
              <span>📅</span>
              <div>
                <small>Today's Learning</small>
                <strong>Keep going!</strong>
              </div>
            </div>
          </section>


          {/* Statistics */}
          <section className="stats-grid">

            <div className="stat-card">
              <div className="stat-icon pdf-icon">
                📄
              </div>

              <div>
                <span>Study Materials</span>
                <h2>5</h2>
                <small>PDFs uploaded</small>
              </div>
            </div>


            <div className="stat-card">
              <div className="stat-icon tutor-icon">
                💬
              </div>

              <div>
                <span>AI Tutor</span>
                <h2>Ask →</h2>
                <small>Get instant explanations</small>
              </div>
            </div>


            <div className="stat-card">
              <div className="stat-icon quiz-icon">
                📝
              </div>

              <div>
                <span>Quiz</span>
                <h2>Start →</h2>
                <small>Test your knowledge</small>
              </div>
            </div>


            <div className="stat-card">
              <div className="stat-icon progress-icon">
                📊
              </div>

              <div>
                <span>Progress</span>
                <h2>78%</h2>
                <small>Overall performance</small>
              </div>
            </div>

          </section>


          {/* Main Dashboard Grid */}
          <section className="dashboard-grid">

            {/* Recent Documents */}
            <div className="dashboard-card documents-card">

              <div className="card-header">
                <div>
                  <h3>📚 Recent Documents</h3>
                  <p>Your recently uploaded study material</p>
                </div>

                <button className="text-button">
                  View all →
                </button>
              </div>

              <div className="document-item">

                <div className="document-icon">
                  📄
                </div>

                <div className="document-info">
                  <strong>Linear Algebra Notes</strong>
                  <span>PDF • 24 pages</span>
                </div>

                <span className="document-status">
                  Ready
                </span>

              </div>


              <div className="document-item">

                <div className="document-icon">
                  📄
                </div>

                <div className="document-info">
                  <strong>Digital Logic</strong>
                  <span>PDF • 42 pages</span>
                </div>

                <span className="document-status">
                  Ready
                </span>

              </div>


              <div className="document-item">

                <div className="document-icon">
                  📄
                </div>

                <div className="document-info">
                  <strong>Quantum Computing</strong>
                  <span>PDF • 31 pages</span>
                </div>

                <span className="document-status">
                  Ready
                </span>

              </div>

            </div>


            {/* Learning Progress */}
            <div className="dashboard-card progress-card">

              <div className="card-header">
                <div>
                  <h3>📊 Learning Progress</h3>
                  <p>Your overall learning performance</p>
                </div>
              </div>

              <div className="progress-circle">

                <div className="progress-inner">
                  <strong>78%</strong>
                  <span>Progress</span>
                </div>

              </div>

              <div className="progress-details">

                <div>
                  <span>Questions</span>
                  <strong>124</strong>
                </div>

                <div>
                  <span>Correct</span>
                  <strong>97</strong>
                </div>

                <div>
                  <span>Accuracy</span>
                  <strong>78%</strong>
                </div>

              </div>

            </div>

          </section>


          {/* Quick Actions */}
          <section className="quick-section">

            <h2>Quick Actions</h2>

            <div className="quick-grid">

              <button className="quick-card">
                <span>📄</span>
                <div>
                  <strong>Upload PDF</strong>
                  <small>Add new study material</small>
                </div>
                <b>→</b>
              </button>


              <button className="quick-card">
                <span>💬</span>
                <div>
                  <strong>Ask AI Tutor</strong>
                  <small>Ask a question</small>
                </div>
                <b>→</b>
              </button>


              <button className="quick-card">
                <span>📝</span>
                <div>
                  <strong>Take a Quiz</strong>
                  <small>Test your knowledge</small>
                </div>
                <b>→</b>
              </button>

            </div>

          </section>

        </main>

      </div>

    </div>
  );
}

export default Dashboard;