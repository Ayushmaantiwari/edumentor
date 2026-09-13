import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../services/api.js";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  async function handleLogin(event) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const data = await loginUser(
        email,
        password
      );

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      localStorage.setItem(
        "user",
        JSON.stringify(data.user)
      );

      navigate("/");
    } catch (error) {
      setError(
        error.message ||
        "Invalid email or password"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-overlay">

      <div className="login-modal">

        {/* ================= LEFT SIDE ================= */}
        <div className="login-left">

          <div className="login-content">

            <h1>Hello Again!</h1>

            <p className="login-subtitle">
              Let's get started with your 30 days trial
            </p>


            <form onSubmit={handleLogin}>

              {/* Email */}
              <div className="login-field">

                <input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  required
                />

              </div>


              {/* Password */}
              <div className="login-field password-field">

                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  required
                />

                <span className="password-icon">
                  ◉
                </span>

              </div>


              {/* Recovery */}
              <div className="recovery-link">
                <span>
                  Recovery Password
                </span>
              </div>


              {/* Error */}
              {error && (
                <div className="login-error">
                  {error}
                </div>
              )}


              {/* Login Button */}
              <button
                type="submit"
                className="login-button"
                disabled={loading}
              >
                {loading
                  ? "Signing In..."
                  : "Sign In"}
              </button>

            </form>


            {/* Divider */}
            <div className="login-divider">

              <span></span>

              <p>
                Or continue with
              </p>

              <span></span>

            </div>


            {/* Social Login */}
            <div className="social-login">

              <button className="social-button">
                G
              </button>

              <button className="social-button apple">
                
              </button>

              <button className="social-button">
                f
              </button>

            </div>


            {/* Register */}
            <p className="register-text">

              Don't have an account?

              <Link to="/register">
                Create Account
              </Link>

            </p>

          </div>

        </div>


        {/* ================= RIGHT SIDE ================= */}
        <div className="login-right">

          <div className="landscape-sky"></div>

          <div className="sun"></div>

          <div className="mountain mountain-one"></div>

          <div className="mountain mountain-two"></div>

          <div className="landscape-ground"></div>

          <div className="tree tree-one"></div>
          <div className="tree tree-two"></div>
          <div className="tree tree-three"></div>
          <div className="tree tree-four"></div>

          <div className="login-quote">
            Finally, your learning journey begins.
          </div>

        </div>

      </div>

    </div>
  );
}

export default Login;