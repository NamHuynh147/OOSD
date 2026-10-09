# AIK-08 - Ứng dụng WinForms xem và điều khiển phiên tra cứu (read-only)

Ứng dụng .NET 8 WinForms (có file `*.Designer.cs`) kết nối PostgreSQL và hiển thị dữ liệu của hệ thống AIK-08
theo tài liệu phân tích và thiết kế: phiên tra cứu, kế hoạch, lời gọi tool, cảnh báo của guard, báo cáo có
trích dẫn và truy vết nguồn, cùng phần quản trị allowlist, hạn mức và danh mục nguồn.

Đây là giao diện cho tầng dữ liệu. Tiến trình agent (orchestrator, LLM, tool) không nằm trong dự án này.

## Chạy

1. Cơ sở dữ liệu có sẵn dữ liệu mẫu, chọn một trong hai cách:
   - Docker: `docker compose up -d` (tự chạy `db/01_schema.sql` rồi `db/02_seed.sql`).
     Làm lại từ đầu: `docker compose down -v && docker compose up -d`.
   - PostgreSQL có sẵn trên máy: tạo database `aik08` rồi chạy hai file:
     ```
     psql -U <user> -d aik08 -f db/01_schema.sql
     psql -U <user> -d aik08 -f db/02_seed.sql
     ```
2. Mở `AIK08.csproj` bằng Visual Studio 2022 (workload ".NET desktop development") rồi bấm F5,
   hoặc chạy `dotnet run` trong thư mục dự án (cần .NET 8 SDK trên Windows).
3. Form kết nối mặc định: `localhost`, cổng `5432`, database `aik08`, tài khoản `aik08`, mật khẩu `aik08`
   (khớp `docker-compose.yml`). Nếu máy đã có PostgreSQL ở cổng 5432, đổi cổng map trong
   `docker-compose.yml` (ví dụ `5433:5432`) và nhập cổng đó.

## Màn hình

| Tab | Chức năng | Use case |
| --- | --- | --- |
| Phiên tra cứu | Danh sách phiên; kế hoạch, lời gọi tool (dòng bị chặn tô đỏ), cảnh báo guard; tạo phiên mới; hủy phiên đang chạy; tự làm mới mỗi 3 giây | UC-01, UC-02, UC-04 |
| Báo cáo và nguồn | Nội dung báo cáo, khẳng định và trạng thái có nguồn; chọn khẳng định để xem bằng chứng gốc, vị trí, thời điểm, cảnh báo injection | UC-03 |
| Quản trị | Allowlist công cụ (chỉ tool đọc), hạn mức mặc định, danh mục nguồn (bật/tắt, thêm nguồn) | UC-05 |

Dữ liệu mẫu có đủ 5 trạng thái phiên (đang chạy, hoàn tất, dừng do hạn mức, đã hủy, lỗi), một lời gọi tool bị
chặn vì ngoài allowlist, một đoạn nghi prompt injection, và một khẳng định chưa có nguồn.

## Ghi chú thiết kế

- Mọi truy vấn dùng tham số (`Db.P`), không ghép chuỗi từ dữ liệu nhập.
- Allowlist và hạn mức được sao vào phiên lúc tạo; sửa chính sách chỉ ảnh hưởng phiên tạo sau đó.
- Bảng `evidence` có trigger chặn UPDATE và DELETE (Evidence bất biến).
- `db/01_schema.sql` tạo vai trò `aik08_tool_reader` chỉ có SELECT trên `sources` và `document_chunks`
  (bỏ qua nếu tài khoản không đủ quyền).
- Bản demo lưu văn bản trong `document_chunks`; thêm cột `embedding vector(...)` nếu dùng pgvector.
