import os
import requests
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
    user_message = payload.message.strip()
    mode = payload.mode or "simple"

    try:
        answer = call_ollama(user_message, mode)
        provider = "ollama-mistral"

    except Exception as e:
        print("LLM error:", e)
        answer = build_placeholder_answer(user_message, mode)
        provider = "placeholder-fallback"

    return ChatResponse(
        answer=answer,
        provider=provider,
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

def call_ollama(user_message: str, mode: str) -> str:
    system_prompt = build_system_prompt(mode)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": f"{system_prompt}\n\nNutzerfrage:\n{user_message}",
            "stream": False,
        },
        timeout=180,
    )

    response.raise_for_status()

    data = response.json()
    answer = data.get("response", "").strip()

    if not answer:
        raise ValueError("Ollama returned an empty response")

    return answer

def build_system_prompt(mode: str) -> str:
    base = """
Du bist Clarity AI.
Du bist ein geduldiger digitaler Helfer für ältere Menschen.

Antworte immer auf Deutsch.
Erkläre alles in sehr einfacher Sprache.
Nutze kurze Sätze.
Gehe Schritt für Schritt vor.
Erkläre Fachwörter sofort.
Sprich respektvoll, aber nicht kindlich.
Stelle höchstens eine Rückfrage.
Gib keine endgültige Rechts-, Finanz- oder Medizinberatung.
Bei wichtigen Entscheidungen empfiehl eine Fachperson oder eine vertraute Person.
""".strip()

    modes = {
        "frag": """
Modus: Frag einfach.
Beantworte die Frage klar und einfach.
Nutze ein kurzes Beispiel aus dem Alltag.
""",
        "mail": """
Modus: Mail-Assistent.
Formuliere eine höfliche E-Mail oder einen Brief.
Nutze eine klare Betreffzeile.
Schreibe nicht zu lang.
""",
        "scam": """
Modus: Scam-Check.
Prüfe, ob die Nachricht nach Betrug aussieht.
Sage klar: eher sicher, unklar, oder gefährlich.
Nenne Warnzeichen.
Gib einfache nächste Schritte.
Sage: Keine Links anklicken. Keine Bankdaten oder Passwörter eingeben.
""",
        "klartext": """
Modus: Klartext.
Erkläre einen Brief oder Text in einfachen Worten.
Sage:
1. Worum geht es?
2. Gibt es eine Frist?
3. Was sollte man als Nächstes tun?
""",
        "technik": """
Modus: Technik-Lotse.
Gib eine einfache Schritt-für-Schritt-Anleitung.
Immer nur kleine Schritte.
Frage nach, wenn wichtige Informationen fehlen.
""",
        "wasseich": """
Modus: Was seh ich?
Fotoerkennung ist in diesem Test noch nicht aktiv.
Erkläre freundlich, dass später Bilder erkannt werden können.
Warne bei unbekannten Pflanzen, Beeren oder Pilzen.
""",
        "simple": """
Modus: Einfache Erklärung.
Antworte kurz, ruhig und verständlich.
""",
    }

    return base + "\n\n" + modes.get(mode, modes["simple"]).strip()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
