const API_BASE = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

async function requestJSON(url, options) {
  let res;

  try {
    res = await fetch(url, options);
  } catch (error) {
    throw new Error(
      `Unable to reach the backend at ${API_BASE}. Make sure the FastAPI server is running.`
    );
  }

  let data;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    throw new Error(data?.detail || `Request failed with status ${res.status}.`);
  }

  return data;
}

export async function analyzeThreat(text) {
  return requestJSON(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

export async function chatWithAssistant(payload) {
  return requestJSON(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
