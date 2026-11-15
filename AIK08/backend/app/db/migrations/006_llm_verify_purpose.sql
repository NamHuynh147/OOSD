-- Ghi nhận riêng lượt gọi LLM dùng cho RAG claim verification.
ALTER TABLE aik08.llm_calls DROP CONSTRAINT IF EXISTS ck_llm_calls_purpose;
ALTER TABLE aik08.llm_calls
    ADD CONSTRAINT ck_llm_calls_purpose
    CHECK (purpose IN ('plan', 'act', 'synthesize', 'verify'));
