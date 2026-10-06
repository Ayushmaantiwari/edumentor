// ==================================================
// EduMentor API Configuration
// ==================================================

const API_BASE_URL =
  "https://edumentor-student-izm38a00n-ayushmaantiwari99-3602s-projects.vercel.app";


// ==================================================
// Generic API Request
// ==================================================

async function apiRequest(endpoint, options = {}) {
  let response;

  try {
    response = await fetch(
      `${API_BASE_URL}${endpoint}`,
      {
        ...options,

        headers: {
          ...(options.headers || {}),
        },
      }
    );
  } catch (error) {
    console.error("API connection error:", error);

    throw new Error(
      "Unable to connect to EduMentor server. Please check your internet connection or try again."
    );
  }

  let data = {};

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      `API request failed: ${response.status}`
    );
  }

  return data;
}


// ==================================================
// Get Authentication Token
// ==================================================

function getToken() {
  return localStorage.getItem("access_token");
}


// ==================================================
// Backend Health
// ==================================================

export async function testBackend() {
  return apiRequest("/api/health");
}


// ==================================================
// User Registration
// ==================================================

export async function registerUser(
  name,
  email,
  password
) {
  return apiRequest(
    "/api/auth/register",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        name,
        email,
        password,
      }),
    }
  );
}


// ==================================================
// User Login
// ==================================================

export async function loginUser(
  email,
  password
) {
  const formData = new URLSearchParams();

  formData.append(
    "username",
    email
  );

  formData.append(
    "password",
    password
  );

  let response;

  try {
    response = await fetch(
      `${API_BASE_URL}/api/auth/login`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
        },

        body: formData.toString(),
      }
    );
  } catch (error) {
    console.error(
      "Login connection error:",
      error
    );

    throw new Error(
      "Unable to connect to EduMentor server."
    );
  }

  let data = {};

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      "Invalid email or password"
    );
  }

  // --------------------------------------------------
  // Save access token
  // --------------------------------------------------

  if (data.access_token) {
    localStorage.setItem(
      "access_token",
      data.access_token
    );
  }

  // --------------------------------------------------
  // Save token type if returned
  // --------------------------------------------------

  if (data.token_type) {
    localStorage.setItem(
      "token_type",
      data.token_type
    );
  }

  return data;
}


// ==================================================
// Logout
// ==================================================

export function logoutUser() {
  localStorage.removeItem(
    "access_token"
  );

  localStorage.removeItem(
    "token_type"
  );

  localStorage.removeItem(
    "user"
  );
}


// ==================================================
// Upload Document
// ==================================================

export async function uploadDocument(
  file
) {
  const token = getToken();

  if (!token) {
    throw new Error(
      "You are not logged in. Please sign in again."
    );
  }

  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  let response;

  try {
    response = await fetch(
      `${API_BASE_URL}/api/documents/upload`,
      {
        method: "POST",

        headers: {
          Authorization:
            `Bearer ${token}`,
        },

        // IMPORTANT:
        // Do NOT manually set Content-Type here.
        // Browser automatically creates the multipart boundary.
        body: formData,
      }
    );
  } catch (error) {
    console.error(
      "Upload connection error:",
      error
    );

    throw new Error(
      "Unable to connect to EduMentor server while uploading the PDF."
    );
  }

  let data = {};

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      `Failed to upload document (${response.status})`
    );
  }

  return data;
}


// ==================================================
// Get Documents
// ==================================================

export async function getDocuments() {
  const token = getToken();

  if (!token) {
    throw new Error(
      "You are not logged in. Please sign in again."
    );
  }

  return apiRequest(
    "/api/documents/",
    {
      method: "GET",

      headers: {
        Authorization:
          `Bearer ${token}`,
      },
    }
  );
}


// ==================================================
// Delete Document
// ==================================================

export async function deleteDocument(
  documentId
) {
  const token = getToken();

  if (!token) {
    throw new Error(
      "You are not logged in. Please sign in again."
    );
  }

  return apiRequest(
    `/api/documents/${documentId}`,
    {
      method: "DELETE",

      headers: {
        Authorization:
          `Bearer ${token}`,
      },
    }
  );
}


// ==================================================
// Generate Quiz
// ==================================================

export async function generateQuiz(
  documentId,
  questionCount = 5,
  difficulty = "medium"
) {
  const token = getToken();

  if (!token) {
    throw new Error(
      "You are not logged in. Please sign in again."
    );
  }

  return apiRequest(
    "/api/quiz/generate",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",

        Authorization:
          `Bearer ${token}`,
      },

      body: JSON.stringify({
        document_id:
          Number(documentId),

        question_count:
          Number(questionCount),

        difficulty:
          difficulty,
      }),
    }
  );
}


// ==================================================
// Submit Quiz
// ==================================================

export async function submitQuiz(
  quizId,
  answers
) {
  const token = getToken();

  if (!token) {
    throw new Error(
      "You are not logged in. Please sign in again."
    );
  }

  return apiRequest(
    "/api/quiz/submit",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",

        Authorization:
          `Bearer ${token}`,
      },

      body: JSON.stringify({
        quiz_id:
          Number(quizId),

        answers:
          answers,
      }),
    }
  );
}


// ==================================================
// Student Analytics
// ==================================================

export async function getAnalyticsOverview() {
  const token = getToken();

  if (!token) {
    throw new Error(
      "You are not logged in. Please sign in again."
    );
  }

  return apiRequest(
    "/api/analytics/overview",
    {
      method: "GET",

      headers: {
        Authorization:
          `Bearer ${token}`,

        "Content-Type":
          "application/json",
      },
    }
  );
}


// ==================================================
// Export API Base URL
// ==================================================

export { API_BASE_URL };