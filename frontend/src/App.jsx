import "./App.css";

import Login from "./Pages/Login.jsx";
import Register from "./Pages/Register.jsx";

import ProtectedRoute from "./components/ProtectedRoute.jsx";
import Layout from "./components/Layout.jsx";

import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Dashboard from "./Pages/Dashboard.jsx";
import Documents from "./Pages/Documents.jsx";
import Tutor from "./Pages/Tutor.jsx";
import Quiz from "./Pages/Quiz.jsx";
import Analytics from "./Pages/Analytics.jsx";
import Settings from "./Pages/Settings.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public routes */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        {/* Protected application */}

        <Route element={<ProtectedRoute />}>

          <Route element={<Layout />}>

            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/documents"
              element={<Documents />}
            />

            <Route
              path="/tutor"
              element={<Tutor />}
            />

            <Route
              path="/quiz"
              element={<Quiz />}
            />

            <Route
              path="/analytics"
              element={<Analytics />}
            />

            <Route
              path="/settings"
              element={<Settings />}
            />

          </Route>

        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;