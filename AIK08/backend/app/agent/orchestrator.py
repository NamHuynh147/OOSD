"""Vòng lặp agent có giới hạn. Mọi lần chạy công cụ đều đi qua GuardedTool.

Bố cục của ``run``: dựng ngữ cảnh -> ``_plan`` -> ``_loop`` -> ``_finalize``. Các bất biến:

* Phiên nào cũng kết thúc bằng một báo cáo (kể cả khi bị hủy, lỗi hay tiến trình chết); báo cáo luôn
  lấy từ bằng chứng đã lưu, không gọi thêm LLM khi hủy.
* Hủy luôn thắng: cờ hủy được kiểm tra đầu mỗi lượt, ngay sau mỗi lời gọi LLM và khi kết thúc.
* Quyết định sai của LLM (tool lạ, văn bản thường, tham số sai, lặp hành động) được ghi thành một bước
  ``blocked_policy`` / ``invalid_arguments`` / ``duplicate`` rồi trả lỗi cho LLM chọn lại; chỉ dừng
  ``policy_violations`` sau ``max_consecutive_violations`` lần liên tiếp.
"""

from __future__ import annotations

import contextlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from app.agent.decision import SYSTEM as ACTION_SYSTEM
from app.agent.decision import parse_action
from app.agent.planner import Planner
from app.agent.report_synthesizer import ReportSynthesizer
from app.config import Settings
from app.core.models import (
    Action,
    LLMCallRecord,
    PlanItem,
    PlanStepStatus,
    Report,
    SessionRecord,
    SessionStatus,
    StepDecision,
    StopReason,
)
from app.core.text import estimate_tokens, truncate
from app.db.sessions import SessionRepository
from app.errors import (
    BudgetExceededError,
    CitationError,
    InvalidStateError,
    InvalidToolArgumentsError,
    RejectedActionError,
    ToolNotAllowedError,
)
from app.evidence.store import EvidenceStore
from app.guards.budget_guard import BudgetGuard
from app.guards.guarded_tool import GuardedTool
from app.guards.tool_policy import ToolPolicy
from app.llm.provider import LLMProvider, timeout_kwargs
from app.llm.traced import TracedLLM
from app.telemetry.otel import set_attributes, span

ToolFactory = Callable[[SessionRecord, BudgetGuard, object, ToolPolicy], Mapping[str, GuardedTool]]

HISTORY_WINDOW = 6  # số kết quả công cụ gần nhất đưa vào prompt chọn hành động
SUMMARY_CHARS = 600
MAX_WARNINGS = 12


@dataclass(slots=True)
class _Run:
    """Trạng thái một lần chạy (không đi ra ngoài orchestrator)."""

    session: SessionRecord
    budget: BudgetGuard
    evidence: EvidenceStore
    allow_llm: bool = True
    tools: Mapping[str, GuardedTool] = field(default_factory=dict)
    plan: list[PlanItem] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)
    warnings: list[str] = field(default_factory=list)
    stop: StopReason = StopReason.ERROR
    rejections: int = 0  # quyết định bị từ chối / tham số sai liên tiếp
    repeats: int = 0  # hành động lặp lại liên tiếp
    tool_errors: int = 0  # lỗi công cụ liên tiếp

    @property
    def sid(self) -> UUID:
        return self.session.id

    def warn(self, message: str) -> None:
        if message not in self.warnings and len(self.warnings) < MAX_WARNINGS:
            self.warnings.append(message)


class AgentOrchestrator:
    """Điều phối lập kế hoạch, gọi công cụ có kiểm soát, bằng chứng, hủy phiên và báo cáo bắt buộc."""

    def __init__(
        self, sessions: SessionRepository, llm: LLMProvider, settings: Settings, tool_factory: ToolFactory
    ) -> None:
        self.sessions = sessions
        self.llm = llm if isinstance(llm, TracedLLM) else TracedLLM(llm)
        self.settings = settings
        self.tool_factory = tool_factory
        self.planner = Planner(self.llm)
        self.synthesizer = ReportSynthesizer(self.llm)

    # ------------------------------------------------------------------ vào/ra
    def run(self, session_id: UUID) -> Report:
        with span("agent.session", {"session.id": str(session_id)}) as current:
            report = self._run(session_id)
            set_attributes(
                current,
                {
                    "session.stop_reason": report.stop_reason.value,
                    "report.status": report.status.value,
                    "report.generated_by": report.generated_by,
                    "report.citations": len(report.citations),
                },
            )
            return report

    def _run(self, session_id: UUID) -> Report:
        session = self.sessions.get(session_id)
        if session is None:
            raise ValueError("Không tìm thấy phiên")
        existing = self.sessions.get_report(session_id)
        if existing is not None:
            return existing
        if session.status is not SessionStatus.PENDING or not self.sessions.mark_running(session_id):
            current = self.sessions.get(session_id)
            if current is not None and current.status is SessionStatus.CANCELLING:
                # Người dùng hủy khi phiên còn pending: không chạy gì, chỉ ghi báo cáo "đã hủy".
                return self.recover(session_id) or self._existing_report(session_id)
            raise ValueError(f"Phiên không ở trạng thái pending: {session.status}")

        budget = BudgetGuard(session.limits, reserve_tokens=self.settings.synthesis_reserve_tokens)
        budget.start()
        ctx = _Run(session, budget, self.sessions.evidence_store(session_id))
        try:
            self._start(ctx)
            self._plan(ctx)
            ctx.stop = self._loop(ctx)
        except BudgetExceededError as exc:
            ctx.stop = _budget_reason(exc.dimension)
            ctx.warn(str(exc))
        except Exception as exc:  # noqa: BLE001 — mọi lỗi đều phải dẫn tới một báo cáo
            if self._cancelled(ctx.sid):  # ghi bị từ chối vì 'cancelling' không phải thất bại
                ctx.stop = StopReason.CANCELLED_BY_USER
            else:
                ctx.stop = StopReason.ERROR
                ctx.warn(f"Agent gặp lỗi ({type(exc).__name__}); báo cáo có thể chỉ là một phần.")
        finally:
            self._close_tools(ctx)
        return self._finalize(ctx)

    @staticmethod
    def _close_tools(ctx: _Run) -> None:
        for tool in ctx.tools.values():
            with contextlib.suppress(Exception):  # đóng client lỗi không được chặn báo cáo
                tool.close()

    def recover(self, session_id: UUID) -> Report | None:
        """Đóng một phiên chưa kết thúc mà không có tiến trình nào đang chạy nó.

        Dùng cho phiên bị hủy khi còn pending, phiên mồ côi sau khi tiến trình chết, hoặc quá hạn. Không
        gọi LLM: báo cáo trích xuất từ bằng chứng đã lưu. Bị hủy -> ``cancelled``, còn lại -> ``failed``.
        """
        session = self.sessions.get(session_id)
        if session is None or session.status.is_terminal:
            return None
        if session.status is SessionStatus.PENDING:
            self.sessions.mark_running(session_id)
            session = self.sessions.get(session_id) or session
            if session.status.is_terminal:
                return None
        ctx = _Run(session, BudgetGuard(session.limits), self.sessions.evidence_store(session_id), allow_llm=False)
        if session.cancel_requested_at is not None or session.status is SessionStatus.CANCELLING:
            ctx.stop = StopReason.CANCELLED_BY_USER
        else:
            ctx.stop = StopReason.ERROR
            ctx.warn(
                "Tiến trình xử lý phiên bị gián đoạn (khởi động lại hoặc quá hạn); "
                "báo cáo chỉ gồm bằng chứng đã thu thập."
            )
        return self._finalize(ctx)

    # ----------------------------------------------------------- chuẩn bị, kế hoạch
    def _start(self, ctx: _Run) -> None:
        policy = ToolPolicy(self.sessions.load_allowlist())
        tools = self.tool_factory(ctx.session, ctx.budget, ctx.evidence, policy)
        # The DB allowlist is authoritative; a factory cannot expand it.
        ctx.tools = {name: tool for name, tool in tools.items() if policy.is_allowed(name)}

    def _plan(self, ctx: _Run) -> None:
        tool_names = tuple(sorted(ctx.tools))
        try:
            ctx.budget.check(extra_tokens=estimate_tokens(ctx.session.query) + 800)
            with span("planner.plan", {"tools": ",".join(tool_names)}) as current:
                ctx.plan, response = self.planner.plan(
                    ctx.session.query, tool_names, timeout_seconds=self._time_limit(ctx)
                )
                set_attributes(current, {"plan.steps": len(ctx.plan)})
            self._record_llm(ctx.sid, response, "plan")
            ctx.budget.charge_tokens(response.input_tokens + response.output_tokens)
        except Exception as exc:  # noqa: BLE001
            ctx.warn(f"Không tạo được kế hoạch LLM hợp lệ; dùng kế hoạch dự phòng ({type(exc).__name__}).")
            ctx.plan = _fallback_plan(tool_names)
        try:
            self.sessions.save_plan(ctx.sid, ctx.plan)
        except InvalidStateError:
            # Bị hủy trong lúc LLM đang lập kế hoạch: CSDL từ chối kế hoạch; vòng lặp sẽ thấy cờ hủy.
            if not self._cancelled(ctx.sid):
                raise

    # ---------------------------------------------------------------- vòng lặp
    def _loop(self, ctx: _Run) -> StopReason:
        while True:
            if self._cancelled(ctx.sid):
                return StopReason.CANCELLED_BY_USER
            if ctx.budget.remaining_seconds <= 0:
                return StopReason.BUDGET_SECONDS
            if ctx.budget.steps_left <= 0:
                return self._after_last_step(ctx)
            outcome = self._one_step(ctx)
            if outcome is not None:
                return outcome

    def _after_last_step(self, ctx: _Run) -> StopReason:
        """Hết bước: cho LLM thêm một lượt chỉ được ``finish`` trước khi coi là cạn ngân sách."""
        if not len(ctx.evidence):
            return StopReason.BUDGET_STEPS
        try:
            action = self._decide(ctx, self._current_plan_item(ctx), finish_only=True)
        except BudgetExceededError as exc:
            return _budget_reason(exc.dimension)
        except Exception:  # noqa: BLE001 — không quyết định được thì giữ lý do hết bước
            return StopReason.BUDGET_STEPS
        if self._cancelled(ctx.sid):
            return StopReason.CANCELLED_BY_USER
        return StopReason.ENOUGH_EVIDENCE if action.is_finish else StopReason.BUDGET_STEPS

    def _one_step(self, ctx: _Run) -> StopReason | None:
        with span("orchestrator.iteration", {"iteration.steps_used": ctx.budget.usage().steps}) as current:
            outcome = self._iteration(ctx)
            set_attributes(current, {"iteration.stop": outcome.value if outcome else "continue"})
            return outcome

    def _iteration(self, ctx: _Run) -> StopReason | None:
        """Một lượt: quyết định -> kiểm tra -> (ghi bước) -> chạy công cụ. ``None`` = đi tiếp."""
        item = self._current_plan_item(ctx)
        try:
            action = self._decide(ctx, item)
        except BudgetExceededError as exc:
            return _budget_reason(exc.dimension)
        except RejectedActionError as exc:
            rejected = Action("tool", exc.requested_tool, exc.arguments, exc.rationale, item.idx if item else None)
            if exc.requested_tool:
                ctx.warn(f"LLM đề xuất tool bị từ chối: {truncate(exc.requested_tool, 60)!r}.")
            return self._reject(ctx, rejected, StepDecision.BLOCKED_POLICY, None, str(exc))
        except Exception as exc:  # noqa: BLE001 — lỗi nhà cung cấp LLM, hết thời gian...
            ctx.warn(f"Không lấy được quyết định LLM ({type(exc).__name__}).")
            return StopReason.ERROR

        # Cờ hủy được kiểm tra lại ngay sau lời gọi LLM chậm: CSDL từ chối bước mới khi 'cancelling'.
        if self._cancelled(ctx.sid):
            return StopReason.CANCELLED_BY_USER
        if action.is_finish:
            return StopReason.ENOUGH_EVIDENCE if len(ctx.evidence) else StopReason.NO_PROGRESS

        guarded = ctx.tools.get(action.tool)
        if guarded is None:
            ctx.warn(f"Tool {action.tool!r} không được khởi tạo cho phiên này.")
            return self._reject(ctx, action, StepDecision.BLOCKED_POLICY, None, "Tool không được khởi tạo")
        signature = action.signature()
        if signature in ctx.seen:
            return self._repeat(ctx, action)
        try:
            guarded.validate(action.arguments)
        except (InvalidToolArgumentsError, ToolNotAllowedError) as exc:
            return self._reject(ctx, action, StepDecision.INVALID_ARGUMENTS, action.tool, str(exc))
        ctx.seen.add(signature)
        return self._run_tool(ctx, guarded, action, item)

    def _decide(self, ctx: _Run, item: PlanItem | None, *, finish_only: bool = False) -> Action:
        instruction = (
            'Hết bước: chỉ được trả {"kind":"finish"}.'
            if finish_only
            else "Chọn công cụ tra cứu phù hợp hoặc finish nếu đã đủ bằng chứng."
        )
        prompt = json.dumps(
            {
                "query": ctx.session.query,
                "plan": [{"idx": p.idx, "title": p.title, "goal": p.goal, "tool_hint": p.tool_hint} for p in ctx.plan],
                "allowed_tools": [{"name": n, "description": t.description} for n, t in ctx.tools.items()],
                "current_plan_step": {"idx": item.idx, "title": item.title, "goal": item.goal} if item else None,
                "prior_tool_results": ctx.history[-HISTORY_WINDOW:],
                "budget_left": {"steps": ctx.budget.steps_left, "seconds": int(ctx.budget.remaining_seconds)},
                "instruction": instruction,
            },
            ensure_ascii=False,
            default=str,
        )
        ctx.budget.check(extra_tokens=estimate_tokens(prompt) + 500)
        response = self.llm.complete(system=ACTION_SYSTEM, user=prompt, purpose="act", **self._llm_timeout(ctx))
        self._record_llm(ctx.sid, response, "act")
        ctx.budget.charge_tokens(response.input_tokens + response.output_tokens)
        return parse_action(response.text, allowed_tools=tuple(sorted(ctx.tools)), plan_idx=item.idx if item else None)

    # ------------------------------------------------ ghi bước bị từ chối / lặp
    def _reject(
        self, ctx: _Run, action: Action, decision: StepDecision, tool_name: str | None, detail: str
    ) -> StopReason | None:
        """Ghi bước bị chặn (blocked_policy / invalid_arguments), báo lỗi cho LLM, dừng nếu liên tiếp quá nhiều."""
        with span(
            "guarded_tool.call",
            {"tool.requested": action.tool, "decision": _blocked_label(decision), "detail": truncate(detail, 200)},
        ):
            stop = self._record_closed_step(ctx, action, decision, tool_name, detail)
        if stop is not None:
            return stop
        ctx.rejections += 1
        ctx.history.append(
            {
                "tool": action.tool or "(không xác định)",
                "error": f"{decision.value}: {truncate(detail, 200)}",
                "hint": "Chỉ dùng tool trong allowed_tools với đúng tham số, hoặc finish.",
            }
        )
        if ctx.rejections >= self.settings.max_consecutive_violations:
            ctx.warn(f"LLM liên tiếp đề xuất hành động không hợp lệ {ctx.rejections} lần; dừng phiên.")
            return StopReason.POLICY_VIOLATIONS
        return None

    def _repeat(self, ctx: _Run, action: Action) -> StopReason | None:
        """LLM lặp lại hành động đã chạy: ghi bước duplicate; lặp lần hai thì kết luận đã đủ bằng chứng."""
        with span("guarded_tool.call", {"tool.requested": action.tool, "decision": "duplicate"}):
            stop = self._record_closed_step(
                ctx, action, StepDecision.DUPLICATE, action.tool, "Hành động đã được chạy trước đó"
            )
        if stop is not None:
            return stop
        ctx.repeats += 1
        if ctx.repeats >= 2:
            ctx.warn("LLM lặp lại hành động đã chạy; dừng và tổng hợp từ bằng chứng đã có.")
            return StopReason.ENOUGH_EVIDENCE if len(ctx.evidence) else StopReason.NO_PROGRESS
        ctx.history.append(
            {
                "tool": action.tool,
                "error": "duplicate_action_blocked",
                "hint": "Hành động này đã chạy; hãy chọn hành động khác hoặc finish.",
            }
        )
        return None

    def _record_closed_step(
        self, ctx: _Run, action: Action, decision: StepDecision, tool_name: str | None, detail: str
    ) -> StopReason | None:
        try:
            ctx.budget.ensure_step_available()
            self.sessions.add_step(ctx.sid, action, decision=decision, tool_name=tool_name, detail=detail)
            ctx.budget.charge_step()
        except BudgetExceededError as exc:
            return _budget_reason(exc.dimension)
        except InvalidStateError:
            if self._cancelled(ctx.sid):
                return StopReason.CANCELLED_BY_USER
            raise
        return None

    # -------------------------------------------------------------- chạy công cụ
    def _run_tool(self, ctx: _Run, guarded: GuardedTool, action: Action, item: PlanItem | None) -> StopReason | None:
        with span("guarded_tool.call", {"tool.requested": action.tool, "decision": "allowed"}) as current:
            outcome = self._run_tool_inner(ctx, guarded, action, item)
            set_attributes(current, {"call.stop": outcome.value if outcome else "continue"})
            return outcome

    def _run_tool_inner(
        self, ctx: _Run, guarded: GuardedTool, action: Action, item: PlanItem | None
    ) -> StopReason | None:
        try:
            ctx.budget.ensure_step_available()
            step = self.sessions.add_step(ctx.sid, action, decision=StepDecision.RUNNING, tool_name=action.tool)
            ctx.budget.charge_step()
        except BudgetExceededError as exc:
            return _budget_reason(exc.dimension)
        except InvalidStateError:
            if self._cancelled(ctx.sid):
                return StopReason.CANCELLED_BY_USER
            raise
        closed = False
        try:
            result = guarded.execute(action.arguments, step_no=step.step_no)
            self.sessions.end_step(ctx.sid, step.step_no, StepDecision.EXECUTED, result.summary[:1800])
            closed = True
            labels = guarded.commit_evidence(step_no=step.step_no)
            if item is not None:
                self.sessions.set_plan_status(ctx.sid, item.idx, PlanStepStatus.DONE)
            ctx.history.append(_history_entry(action, result, labels))
            ctx.rejections = ctx.repeats = ctx.tool_errors = 0
        except BudgetExceededError as exc:
            if not closed:
                self.sessions.end_step(ctx.sid, step.step_no, StepDecision.TOOL_ERROR, str(exc))
            return _budget_reason(exc.dimension)
        except Exception as exc:  # noqa: BLE001
            detail = f"{type(exc).__name__}: {str(exc)[:300]}"
            if not closed:
                self.sessions.end_step(ctx.sid, step.step_no, StepDecision.TOOL_ERROR, detail)
            ctx.history.append({"tool": action.tool, "error": detail})
            ctx.tool_errors += 1
            if ctx.tool_errors >= self.settings.max_consecutive_violations:
                ctx.warn(f"Công cụ lỗi liên tiếp {ctx.tool_errors} lần; dừng phiên.")
                return StopReason.ERROR
        return None

    # --------------------------------------------------------------- kết thúc
    def _finalize(self, ctx: _Run) -> Report:
        """Ghi báo cáo + đóng phiên. Hủy luôn thắng; báo cáo bị CSDL từ chối thì ghi bản rút gọn."""
        cancelled = ctx.stop is StopReason.CANCELLED_BY_USER or self._cancelled(ctx.sid)
        if cancelled:
            ctx.stop = StopReason.CANCELLED_BY_USER
            ctx.warn("Phiên bị người dùng hủy; báo cáo chỉ gồm phần bằng chứng đã thu thập được.")
        try:
            saved = tuple(ctx.evidence.all())
        except Exception as exc:  # noqa: BLE001
            saved = ()
            ctx.warn(f"Không đọc lại được bằng chứng ({type(exc).__name__}).")

        remaining = ctx.budget.remaining_seconds
        estimate = estimate_tokens(ctx.session.query + " " + " ".join(e.content[:1500] for e in saved)) + 3000
        if cancelled or not ctx.allow_llm:
            use_llm, skip = False, ""  # hủy/phục hồi: trả ngay phần đã có, không thêm lượt gọi LLM
        elif remaining < self.settings.min_synthesis_seconds:
            use_llm, skip = False, "Còn quá ít thời gian cho bước gọi LLM tổng hợp."
        elif not ctx.budget.can_afford(estimate, reserve=False):
            use_llm, skip = False, "Ngân sách không đủ cho bước gọi LLM tổng hợp."
        else:
            use_llm, skip = True, ""
        timeout = min(self.settings.llm_timeout_seconds, max(1.0, remaining / 2)) if use_llm else None
        draft, synth_response = self.synthesizer.synthesize(
            ctx.session.query,
            saved,
            warnings=tuple(ctx.warnings),
            use_llm=use_llm,
            llm_skip_reason=skip,
            timeout_seconds=timeout,
        )
        for response, purpose in (
            (synth_response, "synthesize"),
            (self.synthesizer.last_verification_response, "verify"),
        ):
            if response is not None:
                try:
                    self._record_llm(ctx.sid, response, purpose)
                    ctx.budget.charge_tokens(response.input_tokens + response.output_tokens)
                except Exception:  # noqa: BLE001, S110 — ghi nhật ký LLM lỗi không được chặn báo cáo
                    pass
        # Nếu việc lập kế hoạch hỏng trước khi kế hoạch được lưu, lưu một kế hoạch tối thiểu hợp lệ.
        try:
            if not self.sessions.get_plan(ctx.sid):
                self.sessions.save_plan(ctx.sid, _fallback_plan(tuple(sorted(ctx.tools))))
        except Exception:  # noqa: BLE001, S110
            pass
        try:
            return self.sessions.finalize(ctx.sid, ctx.stop, draft)
        except CitationError as exc:
            minimal = self.synthesizer.minimal(
                ctx.session.query,
                len(saved),
                draft.warnings
                + (f"Báo cáo đầy đủ bị CSDL từ chối ({exc.constraint or 'trích dẫn'}); đã ghi bản rút gọn.",),
            )
            return self.sessions.finalize(ctx.sid, ctx.stop, minimal)

    # ----------------------------------------------------------------- tiện ích
    def _current_plan_item(self, ctx: _Run) -> PlanItem | None:
        items = self.sessions.get_plan(ctx.sid)
        pending = [p for p in items if p.status is PlanStepStatus.PENDING]
        if pending:
            return pending[0]
        return items[-1] if items else None

    def _cancelled(self, session_id: UUID) -> bool:
        try:
            return bool(self.sessions.is_cancel_requested(session_id))
        except Exception:  # noqa: BLE001
            return False

    def _time_limit(self, ctx: _Run) -> float:
        """Timeout mỗi lời gọi LLM = min(timeout cấu hình, thời gian còn lại của phiên)."""
        return min(self.settings.llm_timeout_seconds, max(0.5, ctx.budget.remaining_seconds))

    def _llm_timeout(self, ctx: _Run) -> dict[str, float]:
        return timeout_kwargs(self.llm, self._time_limit(ctx))

    def _existing_report(self, session_id: UUID) -> Report:
        report = self.sessions.get_report(session_id)
        if report is None:
            raise ValueError("Phiên đã kết thúc nhưng chưa có báo cáo")
        return report

    def _record_llm(self, session_id: UUID, response: Any, purpose: str) -> None:
        self.sessions.record_llm_call(
            session_id,
            LLMCallRecord(
                purpose=purpose,
                provider=response.provider,
                model=response.model,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                duration_ms=response.duration_ms,
            ),
        )


def _history_entry(action: Action, result: Any, labels: tuple[str, ...]) -> dict[str, Any]:
    """Kết quả công cụ đưa vào prompt lượt sau: chỉ tóm tắt + định danh nguồn, không đưa toàn văn."""
    items = result.data if isinstance(result.data, list) else [result.data]
    brief = []
    for it in items[:10]:
        if not isinstance(it, Mapping):
            continue
        # Mục bị gắn cờ injection: chỉ giữ định danh, không đưa tiêu đề/URL (có thể chứa lệnh) vào prompt.
        keys = ("doc_id",) if it.get("prompt_injection_flagged") else ("doc_id", "title", "source_uri")
        brief.append({k: truncate(str(it[k]), 120) for k in keys if k in it})
    # Tóm tắt của công cụ có thể chứa tiêu đề tài liệu: khi kết quả bị gắn cờ thì không đưa nó vào prompt.
    summary = (
        "Kết quả bị gắn cờ prompt injection; nội dung bị ẩn khỏi ngữ cảnh."
        if result.flagged
        else truncate(result.summary, SUMMARY_CHARS)
    )
    return {
        "tool": action.tool,
        "summary": summary,
        "items": brief,
        "evidence_labels": list(labels),
        "flagged": result.flagged,
    }


def _fallback_plan(allowed_tools: tuple[str, ...]) -> list[PlanItem]:
    search = (
        "search_documents" if "search_documents" in allowed_tools else (allowed_tools[0] if allowed_tools else None)
    )
    read = "read_document" if "read_document" in allowed_tools else search
    return [
        PlanItem(1, "Xác định phạm vi", "Xác định nội dung cần tra cứu", search),
        PlanItem(2, "Thu thập bằng chứng", "Tìm nguồn liên quan", search),
        PlanItem(3, "Đối chiếu và tổng hợp", "Kiểm tra nguồn và tổng hợp kết quả", read),
    ]


def _blocked_label(decision: StepDecision) -> str:
    return "blocked" if decision is StepDecision.BLOCKED_POLICY else decision.value


def _budget_reason(dimension: str) -> StopReason:
    return {
        "steps": StopReason.BUDGET_STEPS,
        "tokens": StopReason.BUDGET_TOKENS,
        "seconds": StopReason.BUDGET_SECONDS,
    }.get(dimension, StopReason.ERROR)
