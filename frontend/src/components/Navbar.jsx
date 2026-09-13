import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const navigate = useNavigate();

  // Check whether user is logged in
  const token = localStorage.getItem("access_token");
  const userData = localStorage.getItem("user");

  const isLoggedIn = !!token;

  // Get user information
  let user = null;

  if (userData) {
    try {
      user = JSON.parse(userData);
    } catch (error) {
      user = null;
    }
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    setIsDropdownOpen(false);

    navigate("/login");
  }

  function goToLogin() {
    setIsDropdownOpen(false);

    navigate("/login");
  }

  return (
    <header className="navbar">

      {/* Logo */}
      <div className="navbar-logo">

        <div className="logo-icon">
          🎓
        </div>

        <div>
          <h2>EduMentor</h2>
          <span>AI Teaching Assistant</span>
        </div>

      </div>


      {/* Right Side */}
      <div className="navbar-right">

        {/* Notification */}
        <button className="notification-button">
          🔔
          <span className="notification-dot"></span>
        </button>


        {/* Profile Section */}
        <div className="profile-container">

          <button
            className="profile"
            onClick={() =>
              setIsDropdownOpen(!isDropdownOpen)
            }
          >

            <div className="profile-avatar">
              {isLoggedIn
                ? user?.name?.charAt(0).toUpperCase() || "A"
                : "?"}
            </div>

            <div className="profile-info">

              <strong>
                {isLoggedIn
                  ? user?.name || "User"
                  : "Guest"}
              </strong>

              <span>
                {isLoggedIn
                  ? "Student"
                  : "Not logged in"}
              </span>

            </div>

            <span className="profile-arrow">
              ▾
            </span>

          </button>


          {/* Dropdown Menu */}
          {isDropdownOpen && (
            <div className="profile-dropdown">

              {isLoggedIn ? (
                <>
                  <div className="dropdown-user-info">

                    <strong>
                      {user?.name || "User"}
                    </strong>

                    <span>
                      {user?.email || ""}
                    </span>

                  </div>

                  <div className="dropdown-divider"></div>

                  <button
                    className="dropdown-item"
                    onClick={logout}
                  >
                    🚪 Logout
                  </button>
                </>
              ) : (
                <>
                  <div className="dropdown-user-info">

                    <strong>
                      Welcome to EduMentor
                    </strong>

                    <span>
                      Please login to continue
                    </span>

                  </div>

                  <div className="dropdown-divider"></div>

                  <button
                    className="dropdown-item"
                    onClick={goToLogin}
                  >
                    🔐 Login
                  </button>
                </>
              )}

            </div>
          )}

        </div>

      </div>

    </header>
  );
}

export default Navbar;