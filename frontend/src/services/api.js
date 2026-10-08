// ==================================================
// EduMentor API Configuration
// ==================================================

const API_BASE_URL =
  "https://edumentor-student-two.vercel.app";


// ==================================================
// Get Authentication Token
// ==================================================

function getToken() {
  return localStorage.getItem("access_token");
}


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
    console.error(
      "API connection error:",
      error
    );

    throw new Error(
      "Unable to connect to EduMentor server. Please check your internet connection or try again."
    );
  }

  // --------------------------------------------------
  // Read response
  // --------------------------------------------------

  let data = {};

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  // --------------------------------------------------
  // Handle API errors
  // --------------------------------------------------

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      `API request failed with status ${response.status}`
    );
  }

  return data;
}


// ==================================================
// Backend Health
// ==================================================

export async function testBackend() {
  return apiRequest(
    "/api/health"
  );
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
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({
        name: name,
        email: email,
        password: password,
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
  const formData =
    new URLSearchParams();

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

        body:
          formData.toString(),
      }
    );
  } catch (error) {
    console.error(
      "Login connection error:",
      error
    );

    throw new Error(
      "Unable to connect to EduMentor server. Please check the backend server and CORS configuration."
    );
  }

  let data = {};

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    console.error(
      "Login failed:",
      response.status,
      data
    );

    throw new Error(
      data.detail ||
      data.message ||
      `Login failed with status ${response.status}`
    );
  }

  if (!data.access_token) {
    console.error(
      "Login response does not contain access_token:",
      data
    );

    throw new Error(
      "Login succeeded but no access token was returned by the server."
    );
  }

  // Save access token
  localStorage.setItem(
    "access_token",
    data.access_token
  );

  // Save token type
  localStorage.setItem(
    "token_type",
    data.token_type || "bearer"
  );

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

  const formData =
    new FormData();

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

        // Do NOT set Content-Type manually.
        // Browser creates multipart boundary.
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
// AI Tutor Chat
// ==================================================

export async function askTutor(
  question,
  documentId,
  topK = 5
) {
  const token = getToken();

  if (!token) {
    throw new Error(
      "You are not logged in. Please sign in again."
    );
  }

  return apiRequest(
    "/api/chat",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",

        Authorization:
          `Bearer ${token}`,
      },

      body: JSON.stringify({
        question: question,

        document_id:
          Number(documentId),

        top_k:
          Number(topK),
      }),
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

export {
  API_BASE_URL
};