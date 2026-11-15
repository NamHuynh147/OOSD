# Trạng thái bản dựng AIK-08

## Đã hoàn tất và đã kiểm chứng (PostgreSQL 16 + pgvector thật, LLM giả lập)
- CSDL: migrations 001–007, trigger (máy trạng thái, ngân sách, báo cáo bắt buộc, `unknown_citation`, bằng chứng append-only + chuỗi băm), hai vai trò đọc/ứng dụng.
- Hủy phiên ở mọi thời điểm (đang chọn hành động, lập kế hoạch, chạy công cụ, tổng hợp chậm, phiên còn `pending`) trả báo cáo một phần; phục hồi phiên mồ côi.
- Chuỗi `[E#]` giả trong câu hỏi/tiêu đề/nội dung không làm hỏng báo cáo; nội dung và tiêu đề bị gắn cờ injection không vào prompt hay báo cáo trích xuất.
- Hành động sai/trùng/tham số sai được ghi thành bước đã đóng; ngân sách bước tính một lần; ngân sách thời gian được áp vào lời gọi LLM.
- `InjectionGuard` có chuẩn hóa chống né tránh; `http_get_api` allowlist tiền tố URL; kiểm chứng RAG thấy mọi nguồn được trích dẫn.
- OpenTelemetry nối vào toàn luồng (profile Jaeger trong compose); `ToolRegistry`; API demo `/demo/*`; mock LLM chạy đủ 3 công cụ và qua kiểm chứng bằng đối chiếu nguyên văn.
- Tìm kiếm tiếng Việt: từ dừng lọc trước khi bỏ dấu, ngưỡng liên quan.
- Frontend: build sạch; nút Hủy cho phiên pending/running, dừng polling khi xong, trạng thái toàn vẹn chuỗi băm, markdown render an toàn, chỉ link http(s).
- Test backend qua trên PostgreSQL thật; `ruff check` sạch; 5 test giao diện Playwright qua (nhập khóa, tạo phiên → báo cáo, hủy phiên).
- API có xác thực API key (`API_KEYS`, fail-closed).

## Số đo (xem `docs/05-bao-cao-kiem-thu.md`)
- Tìm kiếm: recall@3 = 100% trên 30 câu (kho 10 tài liệu — dễ); câu ngoài phạm vi trả rỗng 5/6.
- Injection (bộ mẫu độc lập, `docs/05`): lần đo đầu 9/48 và 15/39; sau khi vá luật theo lô A/B thì ~100% trên chính chúng, nhưng **lô held-out C chỉ 5/31 (16%)**, 0/30 báo nhầm. Guard chỉ là tín hiệu phụ; phòng thủ chính là chính sách công cụ (có test chứng minh).

## Chưa kiểm chứng / cần làm
- `docker compose up` và build ảnh Docker chưa chạy (không có Docker daemon); cấu hình compose chỉ qua `docker compose config`.
- Chưa gọi Gemini/OpenRouter thật; chất lượng RAG verifier thật chưa được đo trên tập claim có nhãn.
- **Thu hồi và cấp lại mọi API key từng nằm trong `backend/.env` của bản cũ** (đã bị loại khỏi gói này).
- Chưa có test tải/nhiều worker; ngân sách token chưa chỉnh theo usage thực.
- API key là khóa dùng chung: không phân quyền theo người dùng, không giới hạn tốc độ.

## Lưu ý
- Không sửa migration đã áp dụng (có kiểm tra checksum); thay đổi CSDL = migration mới.
