// Put this into your GitHub Pages frontend JS.
// Replace the API_URL with your real ngrok HTTPS URL.

const API_URL = "https://YOUR-NGROK-URL.ngrok-free.app/chat";

async function askBackend(message, mode = "simple") {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message, mode })
  });

  if (!response.ok) {
    throw new Error("Backend request failed");
  }

  const data = await response.json();
  return data.answer;
}
