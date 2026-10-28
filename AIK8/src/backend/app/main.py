import asyncio
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace

from app.api.schemas import EvidenceResponse, SessionCreate, SessionResponse, StepResponse
from app.config import get_settings
from app.core.orchestrator import AgentOrchestrator
from app.core.session import SessionState
from app.db.session import create_pool
from app.llm.openai_provider import OpenAIProvider
from app.telemetry.otel import configure_telemetry
from app.tools.document_search import DocumentSearchTool
from app.tools.http_get_api import HttpGetApiTool
from app.guards.tool_policy import ToolPolicy

settings = get_settings()
configure_telemetry()
tracer = trace.get_tracer(__name__)
sessions: dict[str, SessionState] = {}
tasks: dict[str, asyncio.Task[None]] = {}
pool: asyncpg.Pool | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global pool
    pool = await create_pool(settings.database_url)
    yield
    if pool is not None:
        await pool.close()


app = FastAPI(title="AIK08 Read-only Agent", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def serialize(session: SessionState) -> SessionResponse:
    return SessionResponse(
        id=session.id,
        question=session.question,
        status=session.status,
        steps=[StepResponse(position=s.position, goal=s.goal, status=s.status) for s in session.steps],
        evidence=[
            EvidenceResponse(id=e.id, source=e.source, content=e.content, flagged=e.flagged)
            for e in session.evidence_items()
        ],
        report=session.report,
        error=session.error,
        used_steps=session.used_steps,
        used_tokens=session.used_tokens,
    )


async def run_session(session: SessionState) -> None:
    if pool is None:
        session.status = "error"
        session.error = "Database connection is not available."
        return
    try:
        provider = OpenAIProvider(settings.openai_api_key, settings.openai_model)
        tools = {
            "document_search": DocumentSearchTool(pool),
            "http_get_api": HttpGetApiTool(set(settings.allowed_api_hosts)),
        }
        unknown_tools = set(settings.allowed_tools) - tools.keys()
        if unknown_tools:
            raise ValueError(f"Configured tool names are not available: {', '.join(sorted(unknown_tools))}")
        orchestrator = AgentOrchestrator(provider, tools, ToolPolicy(set(settings.allowed_tools)))
        with tracer.start_as_current_span("agent.session") as span:
            span.set_attribute("session.id", session.id)
            await orchestrator.run(session)
    except Exception as exc:
        session.status = "error"
        session.error = str(exc)


@app.post("/api/sessions", response_model=SessionResponse, status_code=202)
async def create_session(request: SessionCreate) -> SessionResponse:
    max_steps = min(request.max_steps or settings.max_steps, settings.max_steps)
    max_tokens = min(request.max_tokens or settings.max_tokens, settings.max_tokens)
    max_seconds = min(request.max_seconds or settings.max_seconds, settings.max_seconds)
    session = SessionState(request.question, max_steps, max_tokens, max_seconds)
    sessions[session.id] = session
    task = asyncio.create_task(run_session(session))
    tasks[session.id] = task
    task.add_done_callback(lambda _: tasks.pop(session.id, None))
    return serialize(session)


@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str) -> SessionResponse:
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    return serialize(session)


@app.post("/api/sessions/{session_id}/cancel", response_model=SessionResponse)
async def cancel_session(session_id: str) -> SessionResponse:
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.status in {"queued", "running"}:
        session.request_cancel()
    return serialize(session)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
