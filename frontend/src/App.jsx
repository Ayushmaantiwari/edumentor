import "./App.css";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Layout from "./components/Layout.jsx";

import Dashboard from "./pages/Dashboard.jsx";
import Documents from "./pages/Documents.jsx";
import Tutor from "./pages/Tutor.jsx";
import Quiz from "./pages/Quiz.jsx";
import Analytics from "./pages/Analytics.jsx";
import Settings from "./pages/Settings.jsx";

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