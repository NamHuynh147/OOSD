-- ============================================================================
-- 007_pgvector_public_schema.optional.sql — đưa extension "vector" ra schema public (TÙY CHỌN)
--
-- 005 chạy với search_path = aik08 nên extension được cài vào schema aik08. Mã ứng dụng và
-- seed gọi `::vector` và toán tử `<=>` với search_path mặc định ("$user", public), nên kiểu
-- và toán tử phải nằm ở public, nếu không seed lỗi `type "vector" does not exist` và tìm
-- kiếm lai vector không chạy. Vai trò ứng dụng cũng cần thấy schema public.
--
-- Cố ý ném lỗi khi chưa có extension: migration tùy chọn lỗi thì bị bỏ qua và thử lại ở lần
-- chạy sau, nhờ vậy không bị đánh dấu "đã áp dụng" khi 005 chưa chạy được.
-- ============================================================================

DO $$
DECLARE
    ns text;
BEGIN
    SELECT n.nspname INTO ns
      FROM pg_extension e JOIN pg_namespace n ON n.oid = e.extnamespace
     WHERE e.extname = 'vector';
    IF ns IS NULL THEN
        RAISE EXCEPTION 'pgvector chưa được cài (005 chưa áp dụng)';
    END IF;
    IF ns <> 'public' THEN
        ALTER EXTENSION vector SET SCHEMA public;
    END IF;
    -- Vai trò chỉ-đọc/ứng dụng ghim search_path = aik08 (003), nên không thấy kiểu và toán tử của vector
    -- ở public: thêm public vào cuối. aik08 vẫn đứng trước nên đối tượng của schema này không bị che.
    EXECUTE format('ALTER ROLE __READER_ROLE__ IN DATABASE %I SET search_path = aik08, public, pg_catalog',
                   current_database());
    EXECUTE format('ALTER ROLE __APP_ROLE__ IN DATABASE %I SET search_path = aik08, public, pg_catalog',
                   current_database());
END
$$;
