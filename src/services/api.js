const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const config = {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      const message =
        data?.detail ||
        data?.message ||
        `Request failed with status ${response.status}`;

      throw new Error(message);
    }

    return data;
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        "Unable to connect to the server. Please make sure the backend is running."
      );
    }

    throw error;
  }
}

/*
 * Citizen profile
 */
export async function createProfile(profileData) {
  return request("/profile", {
    method: "POST",
    body: JSON.stringify(profileData),
  });
}

export async function getProfile(userId) {
  return request(`/profile/${userId}`);
}

export async function updateProfile(userId, profileData) {
  return request(`/profile/${userId}`, {
    method: "PUT",
    body: JSON.stringify(profileData),
  });
}

/*
 * Eligibility
 */
export async function checkEligibility(profileData) {
  return request("/eligibility/check", {
    method: "POST",
    body: JSON.stringify(profileData),
  });
}

export async function checkSchemeEligibility(schemeId, profileData) {
  return request(`/eligibility/check/${schemeId}`, {
    method: "POST",
    body: JSON.stringify(profileData),
  });
}

/*
 * Schemes
 */
export async function getSchemes() {
  return request("/schemes");
}

export async function getScheme(schemeId) {
  return request(`/schemes/${schemeId}`);
}

/*
 * Health check
 */
export async function healthCheck() {
  return request("/health");
}

/*
 * History
 */
export async function getHistory() {
  return request("/profile/history");
}

export async function deleteHistory(historyId) {
  return request(`/profile/history/${historyId}`, {
    method: "DELETE",
  });
}

const api = {
  createProfile,
  getProfile,
  updateProfile,
  checkEligibility,
  checkSchemeEligibility,
  getSchemes,
  getScheme,
  getHistory,
  deleteHistory,
  healthCheck,
};

export default api;