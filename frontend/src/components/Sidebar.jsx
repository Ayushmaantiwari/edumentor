import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">

      <nav>

        <p className="sidebar-title">
          MAIN MENU
        </p>

        <ul className="sidebar-menu">

          <li>
            <NavLink to="/">
              <span>🏠</span>
              <span>Dashboard</span>
            </NavLink>
          </li>

          <li>
            <NavLink to="/documents">
              <span>📚</span>
              <span>Documents</span>
            </NavLink>
          </li>

          <li>
            <NavLink to="/tutor">
              <span>💬</span>
              <span>AI Tutor</span>
            </NavLink>
          </li>

          <li>
            <NavLink to="/quiz">
              <span>📝</span>
              <span>Quiz</span>
            </NavLink>
          </li>

          <li>
            <NavLink to="/analytics">
              <span>📊</span>
              <span>Analytics</span>
            </NavLink>
          </li>

        </ul>

        <p className="sidebar-title sidebar-settings-title">
          SYSTEM
        </p>

        <ul className="sidebar-menu">

          <li>
            <NavLink to="/settings">
              <span>⚙️</span>
              <span>Settings</span>
            </NavLink>
          </li>

        </ul>

      </nav>

      <div className="sidebar-help">

        <div className="help-icon">
          💡
        </div>

        <strong>
          Need Help?
        </strong>

        <p>
          Ask EduMentor anything about your studies.
        </p>

        <NavLink
          to="/tutor"
          className="help-button"
        >
          Ask AI Tutor →
        </NavLink>

      </div>

    </aside>
  );
}

export default Sidebar;