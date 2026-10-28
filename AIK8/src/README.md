# AIK08 Read-only Agent

Scaffold for a bounded research agent with a FastAPI backend and React interface. The agent can only use registered read-only tools, keeps immutable evidence, flags suspicious source content, and returns partial reports when cancelled.

## Requirements

- Python 3.11+
- Node.js 20+
- Docker Desktop (for the local PostgreSQL and OpenTelemetry services)
- An OpenAI API key to run live research sessions

## Run locally

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Start PostgreSQL and the OpenTelemetry collector:

   ```powershell
   docker compose up -d
   ```

3. Start the API from the project root:

   ```powershell
   cd backend
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. In another terminal, start the UI:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

   Open <http://localhost:5173>. The API is available at <http://localhost:8000/docs>.

## Safety and limits

- Database access uses a dedicated role with `SELECT` only. The document adapter contains read-only SQL.
- The tool registry is explicit; unknown tool names are rejected. The HTTP adapter only accepts `GET` requests to hosts in `ALLOWED_API_HOSTS`.
- Per-session defaults are 10 steps, 20,000 estimated tokens, and 60 seconds. Requests can lower these limits but cannot raise them.
- Evidence entries are frozen and stored append-only for the lifetime of the API process.
- Retrieved text is marked when it resembles prompt injection and is passed to the report model as untrusted evidence, never as instructions.
- Session data is currently in memory and is lost when the API process restarts. Use a persistent session repository before production deployment.

## Tests

```powershell
cd backend
pytest
```
