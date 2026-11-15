-- ============================================================================
-- 005_pgvector.optional.sql — Vector store (TÙY CHỌN)
--
-- Cần extension "vector" (pgvector). Nếu máy chủ không có, migrate.py bỏ qua file này
-- và hệ thống chạy với tìm kiếm toàn văn (tsvector) — không mất chức năng.
-- Ảnh Docker kèm sẵn: pgvector/pgvector:pg16.
--
-- Embedding mặc định là băm từ (HashingEmbedder, 256 chiều) để chạy offline; thay bằng
-- mô hình nhúng thật bằng cách đổi EmbeddingProvider và số chiều ở đây.
-- ============================================================================

SET search_path = aik08, pg_catalog;

CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE documents ADD COLUMN embedding vector(256);
-- Vector toàn số 0 vô nghĩa với khoảng cách cosine: chặn ngay ở CSDL.
ALTER TABLE documents ADD CONSTRAINT ck_documents_embedding_nonzero
    CHECK (embedding IS NULL OR vector_norm(embedding) > 0);
CREATE INDEX ix_documents_embedding ON documents USING hnsw (embedding vector_cosine_ops);
