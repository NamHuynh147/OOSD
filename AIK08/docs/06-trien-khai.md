# 06 · Triển khai

## Chuẩn bị
```bash
python scripts/init_env.py          # sinh mật khẩu ngẫu nhiên vào .env và backend/.env (không ghi đè)
```
Điền khóa LLM thật vào `backend/.env` nếu không dùng `LLM_PROVIDER=mock`. **Không bao giờ** đưa `.env` vào Git/zip (`scripts/package.py` từ chối đóng gói).

## Docker Compose
```bash
docker compose up --build                          # db (pgvector) + migrate/seed + backend + frontend
OTEL_EXPORTER=otlp docker compose --profile tracing up --build   # thêm Jaeger: http://127.0.0.1:16686
docker compose --profile tools up                  # thêm pgAdmin
```
- Biến bắt buộc dùng `${VAR:?}` nên thiếu mật khẩu sẽ báo lỗi thay vì chạy với giá trị mặc định.
- Backend chạy bằng người dùng không phải root (uid 10001); frontend build nhiều giai đoạn rồi phục vụ bằng nginx.
- Cổng chỉ mở trên `127.0.0.1`.

## Chạy cục bộ không Docker
```bash
cd backend && pip install -r requirements.txt
python -m app.db.migrate --seed        # tạo schema, vai trò, seed
API_KEYS=<khóa-dài-16-ký-tự-trở-lên> LLM_PROVIDER=mock uvicorn app.api.main:app --port 8000
cd ../frontend && npm ci && npm run dev
```
pgvector là tùy chọn: thiếu extension thì migration 005/007 bị bỏ qua và tìm kiếm chạy ở chế độ FTS.

## Biến cấu hình chính
| Biến | Ý nghĩa |
|---|---|
| `OWNER/READER/APP_DATABASE_URL` | DSN ba vai trò |
| `API_KEYS` | Khóa API (phân tách bằng dấu phẩy, mỗi khóa >= 16 ký tự); bắt buộc, thiếu thì backend không khởi động |
| `API_AUTH_DISABLED` | `true` chỉ để chạy thử cục bộ |
| `LLM_PROVIDER` | `mock` \| `google` \| `openai` \| `multi` |
| `PUBLIC_BASE_URL`, `ENABLE_DEMO_API` | API demo `/demo/*` cho `http_get_api` |
| `API_ALLOWED_URL_PREFIXES` | Tiền tố URL được phép gọi (mặc định `<PUBLIC_BASE_URL>/demo/`) |
| `RECOVER_ON_START`, `ORPHAN_GRACE_SECONDS`, `SWEEP_INTERVAL_SECONDS` | Khôi phục phiên mồ côi |
| `MIN_SYNTHESIS_SECONDS` | Thời gian tối thiểu dành cho tổng hợp báo cáo |
| `OTEL_EXPORTER`, `OTEL_EXPORTER_OTLP_ENDPOINT` | `none` \| `console` \| `otlp` |

## Việc phải làm trước khi đưa vào vận hành thật
1. **Thu hồi và cấp lại** mọi API key từng nằm trong `backend/.env` của bản cũ.
2. API đã có xác thực bằng API key dùng chung (không phân quyền theo người dùng, không giới hạn tốc độ, không có thu hồi theo thời gian): nếu mở ra ngoài máy cục bộ hãy đặt sau reverse proxy có TLS và giới hạn tốc độ.
3. Chạy `docker compose up` và kiểm thử với LLM thật; đo chất lượng RAG verifier trên tập claim có nhãn.
