-- ============================================================================
-- 004_seed_allowed_tools.sql — Dữ liệu allowlist công cụ (nguồn sự thật duy nhất)
--
-- Thêm nguồn mới = viết adapter mới + thêm một dòng ở đây (không sửa orchestrator).
-- CHECK ck_allowed_tools_read_only / ck_allowed_tools_no_write_verbs từ chối mọi
-- công cụ không chỉ-đọc, nên không thể "lỡ tay" thêm write tool.
-- ============================================================================

SET search_path = aik08, pg_catalog;

INSERT INTO allowed_tools (name, description) VALUES
    ('search_documents', 'Tìm tài liệu liên quan trong kho tri thức nội bộ (SELECT: toàn văn + vector). Chỉ đọc.'),
    ('read_document',    'Đọc toàn văn một tài liệu theo mã (SELECT theo khóa chính). Chỉ đọc.'),
    ('http_get_api',     'Gọi API ngoài bằng HTTP GET tới máy chủ trong danh sách cho phép. Chỉ đọc.')
ON CONFLICT (name) DO NOTHING;
