import os
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn


# Change this to your exact GitHub Pages origin.
# Example: https://clarity-ai-code.github.io
ALLOWED_ORIGINS = [
    os.getenv("FRONTEND_ORIGIN", "https://clarity-ai-code.github.io"),
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI(title="Clarity AI Test Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    mode: str | None = "simple"


class ChatResponse(BaseModel):
    answer: str
    provider: str
    timestamp: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Clarity AI backend is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request):
    """
    Temporary placeholder endpoint.

    Later, replace build_placeholder_answer() with a call to:
    - Ollama
    - Hugging Face local model
    - Mistral API
    - another LLM backend
    """
    user_message = payload.message.strip()

    answer = build_placeholder_answer(user_message, payload.mode)

    return ChatResponse(
        answer=answer,
        provider="placeholder-backend",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def build_placeholder_answer(message: str, mode: str | None) -> str:
    if mode == "steps":
        return (
            "Ich habe deine Frage erhalten.\n\n"
            "Schritt 1: Ich lese die Frage.\n"
            "Schritt 2: Später wird hier das lokale KI-Modell antworten.\n"
            "Schritt 3: Im Moment ist dies nur ein Test.\n\n"
            f"Deine Frage war: {message}"
        )

    if mode == "scam_check":
        return (
            "Ich kann später prüfen, ob eine Nachricht verdächtig wirkt.\n\n"
            "Für den Test gilt:\n"
            "- Klicke nicht auf unbekannte Links.\n"
            "- Gib keine Passwörter oder Bankdaten ein.\n"
            "- Frage im Zweifel eine vertraute Person.\n\n"
            f"Getesteter Text: {message}"
        )

    return (
        "Ich habe deine Nachricht erhalten.\n\n"
        "Die Verbindung von der Website zum Backend funktioniert.\n"
        "Als nächstes können wir hier ein lokales KI-Modell anschließen.\n\n"
        f"Deine Nachricht war: {message}"
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
