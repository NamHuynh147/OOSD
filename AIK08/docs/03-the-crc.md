# 03 · Thẻ CRC (Class – Responsibility – Collaborators)

| Lớp | Trách nhiệm | Cộng tác với |
|---|---|---|
| `AgentOrchestrator` | Chạy một phiên: lập kế hoạch → vòng lặp lượt → tổng hợp; mọi lối ra đều ghi báo cáo; xử lý hủy; `recover()` cho phiên mồ côi | `SessionRepository`, `Planner`, `GuardedTool`, `ReportSynthesizer`, `BudgetGuard` |
| `SessionRecovery` | Định kỳ/khi khởi động tìm phiên mồ côi (theo tuổi) và đóng chúng bằng `recover()` | `SessionRepository`, `AgentOrchestrator` |
| `Planner` | Xin LLM kế hoạch 3–6 bước, phân tích JSON, có kế hoạch dự phòng | `LLMProvider` |
| `GuardedTool` | Cổng duy nhất tới công cụ: allowlist, tham số, ngân sách, quét injection (nội dung/tiêu đề/URL), hoãn lưu bằng chứng tới khi bước `executed` | `ToolPolicy`, `BudgetGuard`, `InjectionGuard`, `EvidenceStore`, công cụ thô |
| `ToolPolicy` | Cho phép/chặn công cụ theo bảng `allowed_tools` | CSDL |
| `BudgetGuard` | Đếm bước/token/giây; báo hết ngân sách | — |
| `InjectionGuard` | Chuẩn hóa văn bản (NFKC, ký tự vô hình, homoglyph, bỏ dấu) rồi so luật; trả findings | — |
| `ToolRegistry` | Đăng ký và khởi tạo công cụ chỉ khi được allowlist cho phép | `GuardedTool` |
| `SearchTool` / `ReadDocumentTool` | Tìm (FTS + vector) và đọc tài liệu qua vai trò chỉ-đọc | `DocumentRepository` |
| `HttpGetApiTool` | GET tới URL trong allowlist **tiền tố**; chặn redirect, content-type lạ, vượt dung lượng/thời gian | `httpx` |
| `EvidenceStore` | Thêm bằng chứng append-only; kiểm chuỗi băm bằng hàm SQL | PostgreSQL |
| `ReportSynthesizer` | Tổng hợp báo cáo `[E#]` từ bằng chứng, vô hiệu hóa chuỗi giống trích dẫn trong dữ liệu không tin cậy, dự phòng trích xuất | `LLMProvider`, `RAGClaimVerifier` |
| `RAGClaimVerifier` | Bảo đảm mọi nguồn được trích dẫn đến được bộ kiểm chứng (chia lô 8); một lô hỏng ⇒ cả báo cáo hỏng | `retriever`, `LLMProvider` |
| `LLMProvider` (`mock`, Gemini, OpenAI-compatible, `multi`) | Sinh văn bản theo mục đích `plan/act/synthesize/verify`, tôn trọng `timeout_seconds` | `TracedLLM` |
| `TracedLLM` | Bọc provider, tạo span `llm.complete` | OpenTelemetry |
| `PostgresSessionRepository` | Toàn bộ SQL ghi/đọc sổ phiên; `request_cancel` xử lý cả phiên `pending` | `Database` |
