# 05 · Báo cáo kiểm thử

Môi trường: PostgreSQL 16 + pgvector cục bộ, Python 3.13, `LLM` giả lập có kịch bản. **Không** gọi Gemini/OpenRouter thật; **không** chạy `docker compose up` (không có Docker daemon ở nơi kiểm thử).

## Kết quả tổng
| Chế độ | Kết quả |
|---|---|
| Có PostgreSQL (`TEST_POSTGRES_ADMIN_URL`) | **127 passed** |
| Không có PostgreSQL | 81 passed, 46 skipped |
| Giao diện (`npm run e2e`, Playwright + Chromium) | 5 passed |
| `ruff check` | sạch |
| `npm ci && npm run build` | thành công |

Test PostgreSQL tự tạo CSDL tạm + vai trò riêng, migrate, seed, rồi xóa — không đụng dữ liệu dev.

## Ma trận kịch bản
| Mã | Kịch bản | Test |
|---|---|---|
| T1 | Luồng đầy đủ mock: 3 công cụ, báo cáo `llm` qua kiểm chứng | `tests/api/test_demo_and_e2e_postgres.py` |
| T2 | Chuỗi băm: công thức Python = CSDL; UPDATE/DELETE bị chặn; sửa lén bị phát hiện | `tests/evidence` |
| T3 | Hủy khi LLM đang chọn hành động (lần 1/2), khi lập kế hoạch, khi công cụ đang chạy, khi tổng hợp chậm | `tests/agent/test_cancel_postgres.py` |
| T4 | Hủy phiên `pending`; phục hồi phiên mồ côi (running/cancelling/pending), idempotent, theo tuổi | `test_cancel_postgres.py`, `test_recovery_postgres.py` |
| T5 | `[E99]`, `[E0]`, `[E999999]` trong câu hỏi/tiêu đề/nội dung — kể cả khi hủy — không làm hỏng báo cáo; nội dung/tiêu đề tiêm lệnh không vào prompt | `test_citation_strings_postgres.py` |
| T6 | Công cụ lạ ⇒ `blocked_policy`; tham số sai ⇒ `invalid_arguments`; 3 liên tiếp ⇒ `policy_violations`; bộ đếm reset | `test_loop_postgres.py` |
| T7 | Hành động lặp, `max_steps=1`, 10 lời gọi khác nhau đều chạy, hết thời gian (LLM chậm), lỗi LLM, tài liệu 63.000 ký tự | `test_loop_postgres.py` |
| T8 | Injection: chuẩn hóa/né tránh, 62 mẫu tự viết + bộ mẫu độc lập 3 lô (A/B/C, 227 câu); phòng thủ chiều sâu khi luật bỏ sót | `tests/guards`, `test_loop_postgres.py` |
| T9 | HTTP tool: allowlist tiền tố, `..`/mã hóa kép, redirect, content-type, dung lượng, tổng thời gian | `tests/tools/test_http_get_api.py` |
| T10 | Kiểm chứng RAG thấy mọi nguồn trích dẫn; chia lô 8 | `tests/llm/test_rag_verifier.py` |
| T11 | Span OpenTelemetry (≥ 8 loại; `decision=blocked`) | `tests/telemetry` |
| T12 | Chất lượng tìm kiếm + hồi quy vai trò chỉ-đọc với pgvector | `tests/eval` |
| T13 | Registry chỉ khởi tạo công cụ được phép | `tests/tools/test_registry.py` |
| T14 | Từ dừng trước khi bỏ dấu, ngưỡng liên quan | `tests/core/test_text.py` |
| T15 | Xác thực API key: thiếu/sai khóa ⇒ 401, `/health` và `/demo` mở, không có khóa thì không khởi động | `tests/api/test_auth.py` |
| T16 | Giao diện (Playwright, Chromium): hỏi khóa, khóa sai, tạo phiên → báo cáo + chuỗi băm, hủy phiên, không thực thi HTML | `frontend/e2e/app.spec.ts` |

## Số đo
- **Tìm kiếm** (30 câu hỏi có nhãn, kho 10 tài liệu): recall@3 = **100%** (FTS và lai FTS+vector). Câu ngoài phạm vi trả rỗng **5/6** (trước khi sửa: 0/6). Kho nhỏ nên recall dễ đạt; đừng ngoại suy cho kho lớn.
- **Injection — bộ mẫu độc lập** (viết theo góc nhìn kẻ tấn công và tài liệu nghiệp vụ thật, không dựa trên các luật; Anh/Việt/Pháp/Tây Ban Nha/Đức/Nga/Trung, mã hóa, leet, base64, nhúng trong JSON/HTML/markdown/code):

  | Lô | Vai trò | Tấn công bắt được | Báo nhầm |
  |---|---|---|---|
  | A (48 + 39 bình thường) | đo lần đầu **trước** khi sửa luật | **9/48 (19%)** | 2/41 |
  | A sau vòng sửa 1 | tập phát triển | 48/48 | 0/39 |
  | B (39 + 40) | đo lần đầu sau vòng 1 | **15/39 (38%)** | 1/40 |
  | B sau vòng sửa 2 | tập phát triển | 39/39 | 0/40 |
  | C (31 + 30) | **held-out, đo một lần** sau vòng 2 | **5/31 (16%)** | 0/30 |

  Kết luận trung thực: con số 33/33 trước đây là do mẫu tự viết theo luật. Trên văn phạm lạ, luật theo mẫu chỉ bắt khoảng **một phần sáu đến hơn một phần ba**; lô A/B đạt ~100% chỉ vì luật đã được vá theo chính chúng. Lô C **không** được dùng để vá tiếp để giữ nó làm số đo trung thực. Vì vậy `InjectionGuard` chỉ là tín hiệu phụ (tripwire); phòng thủ chính là cấu trúc: công cụ chỉ đọc, allowlist công cụ và URL, ngân sách, bằng chứng nằm ngoài chỉ thị, kiểm chứng trích dẫn. Test `test_defence_in_depth_when_llm_obeys_an_injection_the_guard_missed` chứng minh khi LLM làm theo lệnh tiêm lọt (gọi xóa/ghi/API ngoài allowlist) thì không hành động nào được thực thi. Hai tài liệu giáo dục trích nguyên câu tấn công được gắn cờ có chủ đích (không phân biệt được với tấn công thật) và không tính vào tỉ lệ báo nhầm.
- **Injection — bộ mẫu cũ** (62 mẫu: 33 tấn công, 29 bình thường): 33/33, 0/29 — lạc quan vì do cùng người viết với luật.
- **Lỗi thật tìm thấy nhờ chạy kiểm thử** (đã sửa): nguyên văn đoạn tiêm lệnh lọt vào prompt tổng hợp qua `findings.excerpt` và qua tóm tắt công cụ; bước bị tính ngân sách đôi; vai trò chỉ-đọc không thấy kiểu `vector` sau khi chuyển extension sang `public`.

## Chưa kiểm chứng
- LLM thật (Gemini/OpenRouter): chỉ kiểm bằng nhà cung cấp giả lập; chất lượng RAG verifier thật chưa được đo.
- `docker compose up` (cả profile `tracing`), build ảnh Docker.
- Tải/đồng thời nhiều worker.
- API key là khóa dùng chung (không phân quyền theo người dùng, không giới hạn tốc độ, không có thu hồi theo thời gian).
