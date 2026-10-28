# Mô hình miền

| Thành phần | Trách nhiệm |
| --- | --- |
| `SessionState` | Trạng thái phiên, giới hạn ngân sách, bước chạy và cờ hủy |
| `PlanStep` / `Planner` | Lưu mục tiêu từng bước; bảo đảm kế hoạch có 3–6 bước |
| `AgentOrchestrator` | Điều phối provider, tool, guard và báo cáo |
| `ReadOnlyTool` | Hợp đồng thực thi chỉ đọc cho adapter dữ liệu |
| `ToolPolicy` / `BudgetGuard` | Chặn tool ngoài allowlist và vượt ngân sách |
| `Evidence` / `EvidenceStore` | Bằng chứng bất biến, có hash và cờ nội dung đáng ngờ |
| `ReportSynthesizer` | Tạo báo cáo và xác thực trích dẫn theo ID bằng chứng |
| `LLMProvider` | Đề xuất kế hoạch/hành động và tổng hợp; không tự thực thi tool |
