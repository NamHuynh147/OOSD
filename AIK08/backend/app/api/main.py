"""FastAPI surface for creating and inspecting read-only agent sessions."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.agent.orchestrator import AgentOrchestrator
from app.agent.recovery import SessionRecovery
from app.api.auth import require_api_key
from app.api.demo import router as demo_router
from app.config import Settings
from app.core.models import Limits
from app.db.documents import PostgresDocumentRepository
from app.db.pool import Database
from app.db.sessions import PostgresSessionRepository
from app.errors import AgentError
from app.llm.provider import build_provider
from app.telemetry.otel import configure_telemetry, shutdown_telemetry
from app.tools.registry import default_registry


class CreateSessionRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2_000)
    max_steps: int | None = Field(default=None, ge=1, le=20)
    max_tokens: int | None = Field(default=None, ge=1_000, le=50_000)
    max_seconds: int | None = Field(default=None, ge=5, le=180)


def _services(request: Request) -> tuple[PostgresSessionRepository, AgentOrchestrator]:
    return request.app.state.sessions, request.app.state.orchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings.from_env()
    settings.validate_auth()
    configure_telemetry(settings.otel_exporter, service_name=settings.otel_service_name)
    db = Database.from_settings(settings, max_size=settings.max_concurrent_sessions + 2)
    db.open()
    if not db.check_schema():
        db.close()
        shutdown_telemetry()
        raise RuntimeError("Không tìm thấy schema AIK08 hoặc allowlist rỗng. Hãy chạy migrations và seed trước.")
    sessions = PostgresSessionRepository(db)
    documents = PostgresDocumentRepository(db, vector_mode=settings.vector_search)
    llm = build_provider(settings)

    registry = default_registry(settings, documents)

    app.state.settings = settings
    app.state.db = db
    app.state.sessions = sessions
    app.state.orchestrator = AgentOrchestrator(sessions, llm, settings, registry.build)
    recovery = SessionRecovery(sessions, app.state.orchestrator, settings)
    if settings.recover_on_start:
        recovery.recover_all(force=True)  # phiên còn dở từ lần chạy trước là mồ côi
    recovery.start()
    try:
        yield
    finally:
        recovery.stop()
        db.close()
        shutdown_telemetry()


app = FastAPI(title="AIK-08 Read-only Agent", version="0.2.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(Settings.from_env().cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)


if Settings.from_env().enable_demo_api:
    app.include_router(demo_router)


api = APIRouter(prefix="/api", dependencies=[Depends(require_api_key)])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aik08-readonly-agent"}


@api.post("/sessions", status_code=202)
def create_session(payload: CreateSessionRequest, background_tasks: BackgroundTasks, request: Request) -> Any:
    sessions, orchestrator = _services(request)
    defaults = request.app.state.settings.limits
    try:
        limits = Limits(
            payload.max_steps or defaults.max_steps,
            payload.max_tokens or defaults.max_tokens,
            payload.max_seconds or defaults.max_seconds,
        )
        session = sessions.create(payload.query.strip(), limits)
        background_tasks.add_task(orchestrator.run, session.id)
        return jsonable_encoder({"session": session, "status_url": f"/api/sessions/{session.id}"})
    except (ValueError, AgentError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@api.get("/sessions")
def list_sessions(request: Request, limit: int = 30) -> Any:
    sessions, _ = _services(request)
    if not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="limit phải từ 1 đến 100")
    return jsonable_encoder(sessions.list_recent(limit))


@api.get("/sessions/{session_id}")
def get_session(session_id: UUID, request: Request) -> Any:
    sessions, _ = _services(request)
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên")
    return jsonable_encoder(
        {
            "session": session,
            "plan": sessions.get_plan(session_id),
            "steps": sessions.list_steps(session_id),
            "report": sessions.get_report(session_id),
        }
    )


@api.post("/sessions/{session_id}/cancel")
def cancel_session(session_id: UUID, request: Request) -> Any:
    sessions, _ = _services(request)
    session = sessions.request_cancel(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên")
    return jsonable_encoder(session)


@api.get("/sessions/{session_id}/evidence")
def get_evidence(session_id: UUID, request: Request) -> Any:
    sessions, _ = _services(request)
    if sessions.get(session_id) is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên")
    store = sessions.evidence_store(session_id)
    report = store.verify_integrity()
    return jsonable_encoder(
        {
            "items": store.all(),
            "integrity": {
                "ok": report.ok,
                "broken": list(report.broken),
                "results": [{"seq": s, "ok": ok, "reason": r} for s, ok, r in report.results],
            },
        }
    )


app.include_router(api)
