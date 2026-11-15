# AIK-08 — Hệ thống điều phối Agent tra cứu chỉ-đọc

Backend Python/FastAPI, PostgreSQL qua psycopg (SQL thuần, không ORM), bộ guard cho công cụ/bằng chứng, OpenTelemetry và frontend React + TypeScript. Tài liệu chi tiết: [`docs/`](docs/) (yêu cầu, mô hình miền, thẻ CRC, kiến trúc, báo cáo kiểm thử, triển khai). Trạng thái và những gì **chưa** kiểm chứng: [`STATUS.md`](STATUS.md).

## Luồng chính

1. `POST /api/sessions` tạo phiên `pending` và giao cho tác vụ nền.
2. Agent chuyển phiên sang `running`, lập kế hoạch 3–6 bước, lưu vào CSDL.
3. Mỗi hành động của LLM được kiểm tra với allowlist trong CSDL; chỉ `GuardedTool` được chạy công cụ.
4. Công cụ chỉ đọc (`search_documents`, `read_document`, `http_get_api`). Kết quả bị quét prompt injection; nội dung bị gắn cờ không bao giờ vào prompt hay báo cáo trích xuất.
5. Bằng chứng được lưu append-only với chuỗi băm SHA-256 do trigger tính.
6. Báo cáo có trích dẫn `[E#]`, được kiểm chứng RAG; lỗi/không đạt ⇒ báo cáo trích xuất dự phòng.
7. Phiên **luôn** kết thúc kèm báo cáo — kể cả khi người dùng hủy (trả phần đã có) hoặc tiến trình chết (phục hồi phiên mồ côi).

## Chạy nhanh bằng Docker

```bash
python scripts/init_env.py        # sinh mật khẩu + API_KEYS ngẫu nhiên vào .env và backend/.env
docker compose up --build         # UI http://127.0.0.1:5173 · API http://127.0.0.1:8000
```

Xem trace: `OTEL_EXPORTER=otlp docker compose --profile tracing up --build` (Jaeger: http://127.0.0.1:16686). Mặc định `LLM_PROVIDER=mock` chạy offline; điền khóa LLM thật vào `backend/.env` để dùng Gemini/OpenAI-compatible.

**Xác thực:** mọi `/api/*` cần header `X-API-Key: <khóa>` (hoặc `Authorization: Bearer`). Khóa lấy từ `API_KEYS` trong `.env`; UI hỏi khóa ở lần mở đầu tiên (giữ trong sessionStorage của tab). Thiếu `API_KEYS` thì backend không khởi động; chỉ khi chạy thử cục bộ mới đặt `API_AUTH_DISABLED=true`. `/health` và `/demo/*` (dữ liệu tĩnh, GET) không cần khóa.

## Chạy không Docker

```bash
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env                                   # rồi chỉnh DSN và đặt API_KEYS=<chuỗi >= 16 ký tự>
python -m app.db.migrate --seed                        # schema, vai trò, 10 tài liệu mẫu
uvicorn app.api.main:app --host 127.0.0.1 --port 8000

cd ../frontend && npm ci && npm run dev                # http://localhost:5173
```

pgvector là tùy chọn: không có extension thì tìm kiếm chạy bằng FTS.

## Kiểm thử

```bash
cd backend && TEST_POSTGRES_ADMIN_URL=postgresql://postgres@127.0.0.1:5432/postgres pytest -q   # cần PostgreSQL; không có thì test `postgres` tự bỏ qua
cd frontend && npx playwright install chromium && npm run e2e   # giao diện: nhập khóa, tạo phiên, báo cáo, hủy; cần DB đã migrate+seed và *_DATABASE_URL trong môi trường
```

## LLM

`LLM_PROVIDER` = `mock` (offline, kịch bản demo, chỉ trích nguyên văn) · `google` · `openai` (mọi endpoint tương thích, ví dụ OpenRouter: đặt `OPENAI_BASE_URL=https://openrouter.ai/api/v1` và khóa OpenRouter vào `OPENAI_API_KEY`) · `multi` (Gemini lập kế hoạch/chọn công cụ, endpoint OpenAI-compatible viết báo cáo). Không đưa `.env` hay khóa vào Git; `scripts/package.py` từ chối đóng gói `.env`.

## API

- `GET /health`
- `POST /api/sessions` — `{"query": "...", "max_steps": 10, "max_tokens": 20000, "max_seconds": 60}`
- `GET /api/sessions?limit=30` · `GET /api/sessions/{id}` (phiên, kế hoạch, bước, báo cáo)
- `POST /api/sessions/{id}/cancel`
- `GET /api/sessions/{id}/evidence` — bằng chứng và `integrity: {ok, broken, results}`
- `GET /demo/status|sla|maintenance` — API demo chỉ-đọc cho `http_get_api` (tắt: `ENABLE_DEMO_API=false`)

## Kiểm thử

```bash
cd backend
pip install -r requirements-dev.txt
pytest                                                   # 74 test chạy offline, 41 test PostgreSQL tự bỏ qua
TEST_POSTGRES_ADMIN_URL=postgresql://postgres@127.0.0.1:5432/postgres pytest   # 115 test
ruff check . && ruff format --check .
```

Test PostgreSQL tự tạo CSDL tạm và vai trò riêng rồi xóa. Kết quả và số đo chi tiết: [`docs/05-bao-cao-kiem-thu.md`](docs/05-bao-cao-kiem-thu.md).

## Ranh giới bảo mật

- API có xác thực bằng API key dùng chung (`API_KEYS`, header `X-API-Key`): không phân quyền theo người dùng, không giới hạn tốc độ. Nếu mở ra ngoài máy cục bộ, đặt sau reverse proxy có TLS và giới hạn tốc độ.
- `InjectionGuard` là heuristic và **chỉ là tín hiệu phụ**: trên bộ mẫu độc lập chưa từng thấy nó chỉ bắt ~16% (xem `docs/05`). Phòng thủ chính là công cụ chỉ đọc, allowlist, ngân sách và kiểm chứng trích dẫn.
- `http_get_api` chỉ gọi URL dưới tiền tố trong `API_ALLOWED_URL_PREFIXES`, chặn redirect, content-type lạ, vượt dung lượng/thời gian.
- Khôi phục phiên mồ côi giả định một tiến trình API (`RECOVER_ON_START=false` khi nhiều worker).
- `mock` chỉ kiểm tra luồng; không đại diện cho chất lượng suy luận của LLM thật.
