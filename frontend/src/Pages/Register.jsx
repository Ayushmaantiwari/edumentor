import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { registerUser } from "../services/api.js";


function Register() {

  const navigate = useNavigate();


  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");


  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  async function handleRegister(event) {

    event.preventDefault();

    setError("");
    setSuccess("");


    if (!name || !email || !password) {

      setError(
        "Please fill in all fields."
      );

      return;
    }


    try {

      setLoading(true);


      const data = await registerUser(
        name,
        email,
        password
      );


      console.log(
        "Registration successful:",
        data
      );


      setSuccess(
        "Account created successfully!"
      );


      setTimeout(() => {

        navigate("/");

      }, 1000);


    } catch (error) {

      console.error(
        "Registration error:",
        error
      );


      setError(
        error.message ||
        "Registration failed."
      );


    } finally {

      setLoading(false);

    }
  }


  return (

    <div className="auth-page">

      <div className="auth-card">

        <h1>Create your EduMentor account</h1>

        <p>
          Start your personalized learning journey.
        </p>


        <form onSubmit={handleRegister}>

          <div className="form-group">

            <label>
              Full Name
            </label>

            <input
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(event) =>
                setName(event.target.value)
              }
            />

          </div>


          <div className="form-group">

            <label>
              Email
            </label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
            />

          </div>


          <div className="form-group">

            <label>
              Password
            </label>

            <input
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
            />

          </div>


          {error && (

            <div className="auth-error">
              {error}
            </div>

          )}


          {success && (

            <div className="auth-success">
              {success}
            </div>

          )}


          <button
            type="submit"
            disabled={loading}
          >

            {loading
              ? "Creating account..."
              : "Create Account"
            }

          </button>

        </form>


        <p className="auth-footer">

          Already have an account?

          {" "}

          <Link to="/login">
            Login
          </Link>

        </p>

      </div>

    </div>

  );
}


export default Register;