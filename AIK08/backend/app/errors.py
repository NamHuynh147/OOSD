"""Ngoại lệ miền của hệ thống.

Hai nhóm:
  * Lỗi do guard trong tiến trình (allowlist, ngân sách, tham số công cụ...).
  * Lỗi do CSDL từ chối (ràng buộc toàn vẹn) — được ``app.db.errors.translate``
    ánh xạ từ SQLSTATE sang các lớp dưới đây, để tầng trên không phụ thuộc psycopg.
"""

from __future__ import annotations

from typing import Literal

BudgetDimension = Literal["steps", "tokens", "seconds"]


class AgentError(Exception):
    """Gốc của mọi lỗi miền."""

    code = "agent_error"


class ConfigurationError(AgentError):
    """Cấu hình/migration không hợp lệ (thiếu vai trò CSDL, migration đã áp dụng bị sửa...)."""

    code = "configuration_error"


# --------------------------------------------------------------------- guards
class ToolNotAllowedError(AgentError):
    code = "tool_not_allowed"

    def __init__(self, tool: str, reason: str = "không nằm trong allowlist") -> None:
        self.tool = tool
        self.reason = reason
        super().__init__(f"Công cụ '{tool}' bị chặn: {reason}.")


class InvalidToolArgumentsError(AgentError):
    code = "invalid_tool_arguments"


class ToolExecutionError(AgentError):
    code = "tool_execution_error"


class BudgetExceededError(AgentError):
    """Hết ngân sách: bước, token hoặc thời gian."""

    code = "budget_exceeded"

    def __init__(self, dimension: BudgetDimension, detail: str = "", *, from_db: bool = False) -> None:
        self.dimension: BudgetDimension = dimension
        self.from_db = from_db
        msg = f"Hết ngân sách {dimension}"
        super().__init__(f"{msg}: {detail}" if detail else msg)


# ------------------------------------------------------------------------ LLM
class LLMError(AgentError):
    code = "llm_error"


class LLMOutputError(LLMError):
    """LLM trả về nội dung không đúng định dạng yêu cầu."""

    code = "llm_output_invalid"


class RejectedActionError(LLMOutputError):
    """Quyết định của LLM bị từ chối (sai định dạng hoặc tool ngoài allowlist).

    Mang theo tên tool được đề xuất để orchestrator ghi lại một bước ``blocked_policy``.
    """

    code = "action_rejected"

    def __init__(
        self, message: str, *, requested_tool: str = "", arguments: object = None, rationale: str = ""
    ) -> None:
        self.requested_tool = requested_tool
        self.arguments = arguments if isinstance(arguments, dict) else {}
        self.rationale = rationale
        super().__init__(message)


# --------------------------------------------------------- vi phạm ràng buộc CSDL
class IntegrityViolation(AgentError):
    """CSDL từ chối thao tác vì vi phạm ràng buộc."""

    code = "integrity_violation"

    def __init__(self, message: str, *, sqlstate: str = "", constraint: str = "", detail: str = "") -> None:
        self.sqlstate = sqlstate
        self.constraint = constraint
        self.detail = detail
        super().__init__(message)


class ConstraintViolation(IntegrityViolation):
    """CHECK / FOREIGN KEY / UNIQUE / NOT NULL (lớp SQLSTATE 23)."""

    code = "constraint_violation"


class PermissionDenied(IntegrityViolation):
    """Vai trò CSDL không đủ quyền (42501) hoặc giao dịch chỉ-đọc (25006)."""

    code = "permission_denied"


class ImmutableViolation(IntegrityViolation):  # AK002
    code = "immutable_violation"


class InvalidStateError(IntegrityViolation):  # AK003
    code = "invalid_state"


class PlanCardinalityError(IntegrityViolation):  # AK004
    code = "plan_cardinality"


class CitationError(IntegrityViolation):  # AK005
    code = "citation_error"


class ReportRequiredError(IntegrityViolation):  # AK006
    code = "report_required"
