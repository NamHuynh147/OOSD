"""2.2 — luồng đầy đủ với công cụ http_get_api qua API demo thật + mock LLM; phiên kết thúc bằng báo cáo 'llm' đã qua kiểm chứng."""

from __future__ import annotations

import dataclasses

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.agent.orchestrator import AgentOrchestrator
from app.api.demo import router
from app.core.models import Limits, SessionStatus, StepDecision
from app.guards.guarded_tool import GuardedTool
from app.guards.injection_guard import InjectionGuard
from app.llm.provider import MockLLMProvider
from app.tools.document_search import DocumentSearchTool, ReadDocumentTool
from app.tools.http_get_api import HttpGetApiTool

BASE = "http://127.0.0.1:8000"


def _demo_client() -> httpx.Client:
    app = FastAPI()
    app.include_router(router)
    # httpx.Client chạy thẳng vào ứng dụng ASGI qua TestClient: không cần mở cổng thật.
    return TestClient(app, base_url=BASE)


def test_demo_routes_are_get_only_static_json():
    client = _demo_client()
    assert client.get("/demo/status").json()["services"][0]["service"] == "thanh-toan"
    assert "targets" in client.get("/demo/sla").json()
    assert "02:00" in client.get("/demo/maintenance").text
    for method in ("post", "put", "delete", "patch"):
        assert getattr(client, method)("/demo/status").status_code == 405


@pytest.mark.postgres
def test_mock_agent_uses_all_three_tools_and_report_passes_verification(sessions, documents, settings):
    client = _demo_client()

    def factory(session, budget, evidence, policy):
        http = HttpGetApiTool(allowed_prefixes=(f"{BASE}/demo/",), client=client)
        raw = [DocumentSearchTool(documents), ReadDocumentTool(documents), http]
        return {
            t.name: GuardedTool(
                t, policy=policy, budget=budget, injection_guard=InjectionGuard(), evidence_store=evidence
            )
            for t in raw
            if policy.is_allowed(t.name)
        }

    orch = AgentOrchestrator(
        sessions, MockLLMProvider(api_base_url=BASE), dataclasses.replace(settings, llm_provider="mock"), factory
    )
    session = sessions.create("Cam kết SLA của dịch vụ thanh toán là bao nhiêu?", Limits(10, 20000, 60))
    report = orch.run(session.id)

    steps = sessions.list_steps(session.id)
    assert [s.requested_tool for s in steps if s.decision is StepDecision.EXECUTED] == [
        "search_documents",
        "read_document",
        "http_get_api",
    ]
    items = sessions.evidence_store(session.id).all()
    assert {e.tool_name for e in items} == {"search_documents", "read_document", "http_get_api"}
    assert sessions.get(session.id).status is SessionStatus.COMPLETED
    assert report.generated_by == "llm" and "Kiểm chứng RAG" in report.markdown
    assert set(report.citations) == {e.seq for e in items if not e.flagged}
