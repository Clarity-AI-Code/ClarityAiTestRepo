# Clarity AI Test Backend

This is a small local backend for testing your GitHub Pages website with a local AI server later.

Current flow:

```txt
GitHub Pages frontend
        ↓
ngrok public URL
        ↓
FastAPI backend on your PC
        ↓
placeholder answer now, local LLM later
```

## 1. Install Python dependencies

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS/Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure environment

Copy `.env.example` to `.env`.

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` if needed.

For your current GitHub Pages site, this is likely correct:

```txt
FRONTEND_ORIGIN=https://clarity-ai-code.github.io
PORT=8000
```

## 3. Start the backend

```bash
python app.py
```

Open this in your browser:

```txt
http://localhost:8000
```

API docs:

```txt
http://localhost:8000/docs
```

## 4. Test locally

In another terminal:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hallo, funktioniert das?\",\"mode\":\"simple\"}"
```

## 5. Start ngrok

Install ngrok first, then run:

```bash
ngrok http 8000
```

ngrok will show an HTTPS forwarding URL, for example:

```txt
https://abc123.ngrok-free.app
```

Your frontend should call:

```txt
https://abc123.ngrok-free.app/chat
```

## 6. Update your GitHub Pages frontend

In your frontend JavaScript, set:

```js
const API_URL = "https://abc123.ngrok-free.app/chat";
```

Commit and push the change.

Then open:

```txt
https://clarity-ai-code.github.io/ClarityAiTestRepo/
```

## Important

For user testing:

- Your PC must stay on.
- The backend must stay running.
- ngrok must stay running.
- The local LLM, once added, must stay running.
- Do not ask testers to enter passwords, bank data, addresses, or sensitive health data.

## Later LLM integration

Replace the `build_placeholder_answer()` call inside `app.py` with a real local model call.

Good later options:

- Ollama local API
- Hugging Face Transformers
- llama.cpp server
- Mistral API for hosted testing
