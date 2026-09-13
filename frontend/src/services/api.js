const API_BASE_URL = "http://localhost:8000";


async function apiRequest(
  endpoint,
  options = {}
) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      },

      ...options
    }
  );

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status}`
    );
  }

  return response.json();
}


// --------------------------------
// Backend Health
// --------------------------------

export async function testBackend() {

  return apiRequest("/api/health");

}

// --------------------------------
// User Registration
// --------------------------------

export async function registerUser(
  name,
  email,
  password
) {
  return apiRequest(
    "/api/auth/register",
    {
      method: "POST",
      body: JSON.stringify({
        name,
        email,
        password
      })
    }
  );
}

// --------------------------------
// User Login
// --------------------------------
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


  const response = await fetch(
    `${API_BASE_URL}/api/auth/login`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded"
      },

      body: formData
    }
  );


  const data = await response.json();


  if (!response.ok) {

    throw new Error(
      data.detail ||
      "Invalid email or password"
    );

  }


  return data;
}

// --------------------------------
// Upload Documents
// --------------------------------
export async function uploadDocument(file) {
  const token = localStorage.getItem("access_token");

  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/documents/upload`,
    {
      method: "POST",

      headers: {
        Authorization: `Bearer ${token}`,
      },

      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to upload document"
    );
  }

  return data;
}

// --------------------------------
// Upload Function
// --------------------------------


export async function getDocuments() {
  const token = localStorage.getItem(
    "access_token"
  );

  const response = await fetch(
    `${API_BASE_URL}/api/documents/`,
    {
      method: "GET",

      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to load documents"
    );
  }

  return data;
}


export async function deleteDocument(
  documentId
) {
  const token = localStorage.getItem(
    "access_token"
  );

  const response = await fetch(
    `${API_BASE_URL}/api/documents/${documentId}`,
    {
      method: "DELETE",

      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to delete document"
    );
  }

  return data;
}


// --------------------------------
// Quiz Generation and Submission
// --------------------------------


export async function generateQuiz(
  documentId,
  questionCount = 5,
  difficulty = "medium"
) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    "http://127.0.0.1:8000/api/quiz/generate",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },

      body: JSON.stringify({
        document_id: Number(documentId),
        question_count: Number(questionCount),
        difficulty: difficulty,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to generate quiz."
    );
  }

  return data;
}


export async function submitQuiz(
  quizId,
  answers
) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    "http://127.0.0.1:8000/api/quiz/submit",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },

      body: JSON.stringify({
        quiz_id: Number(quizId),
        answers: answers,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to submit quiz."
    );
  }

  return data;
}

// --------------------------------
// Student Analytics
// --------------------------------

export async function getAnalyticsOverview() {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    "http://127.0.0.1:8000/api/analytics/overview",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));

    throw new Error(
      errorData.detail || "Failed to load analytics."
    );
  }

  return response.json();
}