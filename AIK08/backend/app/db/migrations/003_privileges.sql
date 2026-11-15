-- ============================================================================
-- 003_privileges.sql — Phân quyền theo vai trò (nguyên tắc đặc quyền tối thiểu)
--
-- Hai vai trò đăng nhập (do app/db/migrate.py tạo trước khi chạy file này).
-- __READER_ROLE__ và __APP_ROLE__ là placeholder: migrate.py thay bằng tên thật lấy từ
-- READER_DATABASE_URL / APP_DATABASE_URL (mặc định aik08_reader / aik08_app). Nhờ vậy
-- kiểm thử tạo được vai trò riêng mà không đụng vai trò của môi trường dev.
--
--   reader  Dùng cho CÔNG CỤ của agent. Chỉ SELECT trên nguồn tri thức,
--           giao dịch mặc định chỉ-đọc, giới hạn thời gian truy vấn.
--           => "Không có write tool" được bảo đảm cả khi mã ứng dụng sai.
--
--   app     Dùng cho việc ghi sổ phiên. Chỉ INSERT vào các bảng nhật ký, và
--           chỉ trên những CỘT ứng dụng được phép cung cấp. Không có quyền
--           UPDATE/DELETE bằng chứng, nhật ký LLM, báo cáo; không đụng tới
--           nguồn tri thức; không ghi được bộ đếm ngân sách.
--
-- Chủ sở hữu (người chạy migration) là bên duy nhất sửa được schema/dữ liệu nguồn.
-- ============================================================================

SET search_path = aik08, pg_catalog;

REVOKE ALL ON SCHEMA aik08 FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA aik08 FROM PUBLIC;
GRANT USAGE ON SCHEMA aik08 TO __READER_ROLE__, __APP_ROLE__;

-- ---- __READER_ROLE__: chỉ đọc nguồn tri thức ----------------------------------
GRANT SELECT ON documents, document_categories TO __READER_ROLE__;

-- ---- __APP_ROLE__: ghi sổ phiên, theo từng cột ---------------------------------
GRANT SELECT ON allowed_tools, agent_sessions, plan_steps, steps, llm_calls,
                evidence, reports, report_citations TO __APP_ROLE__;

-- Phiên: chỉ cung cấp nội dung yêu cầu + hạn mức; trạng thái đổi qua UPDATE có kiểm soát.
GRANT INSERT (query, max_steps, max_tokens, max_seconds) ON agent_sessions TO __APP_ROLE__;
GRANT UPDATE (status, stop_reason)                         ON agent_sessions TO __APP_ROLE__;

GRANT INSERT (session_id, idx, title, goal, tool_hint) ON plan_steps TO __APP_ROLE__;
GRANT UPDATE (status)                                  ON plan_steps TO __APP_ROLE__;

GRANT INSERT (session_id, requested_tool, tool_name, arguments, rationale, plan_idx, decision, detail)
    ON steps TO __APP_ROLE__;
GRANT UPDATE (decision, detail) ON steps TO __APP_ROLE__;

GRANT INSERT (session_id, purpose, provider, model, input_tokens, output_tokens, duration_ms)
    ON llm_calls TO __APP_ROLE__;

-- Bằng chứng: KHÔNG cho cung cấp seq / hash / thời điểm — CSDL tự tính.
GRANT INSERT (session_id, step_no, source_uri, title, content, raw_sha256, flagged, findings)
    ON evidence TO __APP_ROLE__;

GRANT INSERT (session_id, status, stop_reason, generated_by, markdown, warnings, steps_completed, steps_planned)
    ON reports TO __APP_ROLE__;
GRANT INSERT (session_id, seq) ON report_citations TO __APP_ROLE__;

-- ---- Cấu hình mức vai trò (áp dụng cho CSDL hiện tại) -----------------------
DO $$
DECLARE
    db text := current_database();
BEGIN
    -- Công cụ agent: giao dịch chỉ-đọc, truy vấn tối đa 5 giây.
    EXECUTE format('ALTER ROLE __READER_ROLE__ IN DATABASE %I SET default_transaction_read_only = on', db);
    EXECUTE format('ALTER ROLE __READER_ROLE__ IN DATABASE %I SET statement_timeout = %L', db, '5s');
    EXECUTE format('ALTER ROLE __READER_ROLE__ IN DATABASE %I SET search_path = aik08, pg_catalog', db);
    -- Ghi sổ phiên: không để giao dịch treo.
    EXECUTE format('ALTER ROLE __APP_ROLE__ IN DATABASE %I SET idle_in_transaction_session_timeout = %L', db, '30s');
    EXECUTE format('ALTER ROLE __APP_ROLE__ IN DATABASE %I SET search_path = aik08, pg_catalog', db);
END
$$;
