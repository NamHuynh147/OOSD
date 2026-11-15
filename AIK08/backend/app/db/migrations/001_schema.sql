-- ============================================================================
-- 001_schema.sql — Lược đồ AIK-08 (PostgreSQL ≥ 14, SQL thuần, không ORM)
--
-- File này chứa bảng + ràng buộc KHAI BÁO: PRIMARY KEY, FOREIGN KEY, UNIQUE,
-- NOT NULL, CHECK. Ràng buộc nghiệp vụ liên bảng (máy trạng thái, ngân sách,
-- bất biến bằng chứng, báo cáo bắt buộc...) nằm ở 002_integrity_triggers.sql.
-- Quyền hạn theo vai trò nằm ở 003_privileges.sql.
--
-- Quy ước tên ràng buộc: pk_ / fk_ / uq_ / ck_ + <bảng> + <ý nghĩa>.
-- Test phụ thuộc vào các tên này (diag.constraint_name) — đừng đổi tùy tiện.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS aik08;
SET search_path = aik08, pg_catalog;

-- ----------------------------------------------------------------------------
-- Hàm tiện ích: bỏ dấu tiếng Việt. IMMUTABLE nên dùng được trong cột sinh
-- (generated column) và chỉ mục. Bảng ánh xạ liệt kê cả chữ hoa lẫn thường để
-- kết quả không phụ thuộc locale của máy chủ.
-- ----------------------------------------------------------------------------
CREATE FUNCTION fold_vi(t text) RETURNS text
LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT
SET search_path = pg_catalog
AS $$
    SELECT translate(
        lower(normalize(t, NFC)),
        'àÀáÁạẠảẢãÃâÂầẦấẤậẬẩẨẫẪăĂằẰắẮặẶẳẲẵẴèÈéÉẹẸẻẺẽẼêÊềỀếẾệỆểỂễỄìÌíÍịỊỉỈĩĨòÒóÓọỌỏỎõÕôÔồỒốỐộỘổỔỗỖơƠờỜớỚợỢởỞỡỠùÙúÚụỤủỦũŨưƯừỪứỨựỰửỬữỮỳỲýÝỵỴỷỶỹỸđĐ',
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaeeeeeeeeeeeeeeeeeeeeeeiiiiiiiiiioooooooooooooooooooooooooooooooooouuuuuuuuuuuuuuuuuuuuuuyyyyyyyyyydd'
    )
$$;

-- ----------------------------------------------------------------------------
-- Nguồn tri thức (chỉ đọc đối với agent)
-- ----------------------------------------------------------------------------
CREATE TABLE document_categories (
    code  text NOT NULL,
    label text NOT NULL,
    CONSTRAINT pk_document_categories PRIMARY KEY (code),
    CONSTRAINT ck_document_categories_code  CHECK (code ~ '^[a-z][a-z_]{1,29}$'),
    CONSTRAINT ck_document_categories_label CHECK (char_length(btrim(label)) BETWEEN 1 AND 100)
);

CREATE TABLE documents (
    doc_id       text        NOT NULL,
    category     text        NOT NULL,
    title        text        NOT NULL,
    body         text        NOT NULL,
    source_uri   text        NOT NULL,
    publisher    text        NOT NULL DEFAULT '',        -- đơn vị ban hành / nguồn gốc (provenance)
    language     text        NOT NULL DEFAULT 'vi',
    published_at date        NOT NULL,
    updated_at   timestamptz NOT NULL DEFAULT now(),
    -- Chỉ mục toàn văn không dấu; cột sinh tự cập nhật, ứng dụng không thể ghi sai.
    fts          tsvector GENERATED ALWAYS AS (to_tsvector('simple', fold_vi(title || ' ' || body))) STORED,
    CONSTRAINT pk_documents PRIMARY KEY (doc_id),
    CONSTRAINT uq_documents_source_uri UNIQUE (source_uri),
    CONSTRAINT fk_documents_category FOREIGN KEY (category)
        REFERENCES document_categories (code) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_documents_doc_id     CHECK (doc_id ~ '^[A-Z]{2,6}-[0-9]{3,6}$'),
    CONSTRAINT ck_documents_title      CHECK (char_length(btrim(title)) BETWEEN 1 AND 300),
    CONSTRAINT ck_documents_body       CHECK (char_length(btrim(body)) BETWEEN 1 AND 200000),
    CONSTRAINT ck_documents_source_uri CHECK (source_uri ~ '^(doc|https?)://[^[:space:]]+$'),
    CONSTRAINT ck_documents_publisher  CHECK (char_length(publisher) <= 200),
    CONSTRAINT ck_documents_language   CHECK (language IN ('vi', 'en')),
    CONSTRAINT ck_documents_published   CHECK (published_at >= DATE '2000-01-01')
);
CREATE INDEX ix_documents_fts      ON documents USING gin (fts);
CREATE INDEX ix_documents_category ON documents (category);

-- ----------------------------------------------------------------------------
-- Allowlist công cụ. Đây là nguồn sự thật duy nhất về công cụ được phép chạy:
--   * steps.tool_name có khóa ngoại tới đây  → bước "executed" luôn là công cụ allowlist;
--   * ck_allowed_tools_read_only             → không thể đăng ký công cụ ghi;
--   * ck_allowed_tools_no_write_verbs        → tên kiểu create_/delete_/write_... bị từ chối.
-- ----------------------------------------------------------------------------
CREATE TABLE allowed_tools (
    name        text NOT NULL,
    description text NOT NULL,
    access      text NOT NULL DEFAULT 'read_only',
    CONSTRAINT pk_allowed_tools PRIMARY KEY (name),
    CONSTRAINT ck_allowed_tools_name        CHECK (name ~ '^[a-z][a-z0-9_]{2,39}$'),
    CONSTRAINT ck_allowed_tools_description CHECK (char_length(btrim(description)) BETWEEN 5 AND 500),
    CONSTRAINT ck_allowed_tools_read_only   CHECK (access = 'read_only'),
    CONSTRAINT ck_allowed_tools_no_write_verbs CHECK (
        name !~ '^(create|update|delete|remove|write|insert|drop|alter|truncate|post|put|patch|send|exec|execute|run|set|save|upload|modify|grant|revoke)(_|$)'
    )
);

-- ----------------------------------------------------------------------------
-- Phiên điều phối agent
-- ----------------------------------------------------------------------------
CREATE TABLE agent_sessions (
    id                  uuid        NOT NULL DEFAULT gen_random_uuid(),
    query               text        NOT NULL,
    status              text        NOT NULL DEFAULT 'pending',
    stop_reason         text,
    -- Hạn mức (mặc định theo đề: 10 bước · 20.000 token · 60 giây; trần cứng ở CHECK)
    max_steps           integer     NOT NULL DEFAULT 10,
    max_tokens          integer     NOT NULL DEFAULT 20000,
    max_seconds         integer     NOT NULL DEFAULT 60,
    -- Bộ đếm: được trigger của steps / llm_calls cập nhật, ứng dụng không ghi trực tiếp
    steps_used          integer     NOT NULL DEFAULT 0,
    tokens_used         integer     NOT NULL DEFAULT 0,
    cancel_requested_at timestamptz,
    created_at          timestamptz NOT NULL DEFAULT clock_timestamp(),
    started_at          timestamptz,
    finished_at         timestamptz,
    CONSTRAINT pk_agent_sessions PRIMARY KEY (id),
    CONSTRAINT ck_sessions_query       CHECK (char_length(btrim(query)) BETWEEN 3 AND 2000),
    CONSTRAINT ck_sessions_status      CHECK (status IN ('pending', 'running', 'cancelling',
                                                         'completed', 'cancelled', 'budget_exhausted', 'failed')),
    CONSTRAINT ck_sessions_max_steps   CHECK (max_steps   BETWEEN 1 AND 20),
    CONSTRAINT ck_sessions_max_tokens  CHECK (max_tokens  BETWEEN 1000 AND 50000),
    CONSTRAINT ck_sessions_max_seconds CHECK (max_seconds BETWEEN 5 AND 180),
    -- Ngân sách bước là ràng buộc cứng: không thể ghi nhận bước thứ max_steps + 1.
    CONSTRAINT ck_sessions_steps_used  CHECK (steps_used BETWEEN 0 AND max_steps),
    CONSTRAINT ck_sessions_tokens_used CHECK (tokens_used >= 0),
    -- Trạng thái kết thúc <=> có finished_at
    CONSTRAINT ck_sessions_finished CHECK (
        (status IN ('completed', 'cancelled', 'budget_exhausted', 'failed')) = (finished_at IS NOT NULL)
    ),
    CONSTRAINT ck_sessions_started CHECK (
        status NOT IN ('running', 'cancelling') OR started_at IS NOT NULL
    ),
    CONSTRAINT ck_sessions_time_order CHECK (
        (started_at  IS NULL OR started_at  >= created_at) AND
        (finished_at IS NULL OR finished_at >= COALESCE(started_at, created_at))
    ),
    -- Lý do dừng phải khớp trạng thái. COALESCE(..., false): CHECK coi NULL là "đạt",
    -- nên stop_reason NULL ở trạng thái kết thúc phải bị ép thành false.
    CONSTRAINT ck_sessions_stop_reason CHECK (
        CASE status
            WHEN 'completed'        THEN COALESCE(stop_reason IN ('enough_evidence', 'plan_done', 'no_progress'), false)
            WHEN 'cancelled'        THEN COALESCE(stop_reason = 'cancelled_by_user', false)
            WHEN 'budget_exhausted' THEN COALESCE(stop_reason IN ('budget_steps', 'budget_tokens', 'budget_seconds'), false)
            WHEN 'failed'           THEN COALESCE(stop_reason IN ('error', 'policy_violations'), false)
            ELSE stop_reason IS NULL
        END
    )
);
CREATE INDEX ix_agent_sessions_created ON agent_sessions (created_at DESC);

-- ----------------------------------------------------------------------------
-- Kế hoạch do Planner tạo (3–6 bước; xem trigger cardinality ở 002)
-- ----------------------------------------------------------------------------
CREATE TABLE plan_steps (
    session_id uuid     NOT NULL,
    idx        smallint NOT NULL,
    title      text     NOT NULL,
    goal       text     NOT NULL DEFAULT '',
    tool_hint  text,
    status     text     NOT NULL DEFAULT 'pending',
    CONSTRAINT pk_plan_steps PRIMARY KEY (session_id, idx),
    CONSTRAINT fk_plan_steps_session   FOREIGN KEY (session_id) REFERENCES agent_sessions (id) ON DELETE RESTRICT,
    CONSTRAINT fk_plan_steps_tool_hint FOREIGN KEY (tool_hint)  REFERENCES allowed_tools (name) ON DELETE RESTRICT,
    CONSTRAINT ck_plan_steps_idx    CHECK (idx BETWEEN 1 AND 6),
    CONSTRAINT ck_plan_steps_title  CHECK (char_length(btrim(title)) BETWEEN 1 AND 300),
    CONSTRAINT ck_plan_steps_status CHECK (status IN ('pending', 'done', 'skipped'))
);

-- ----------------------------------------------------------------------------
-- Dòng thời gian các hành động agent đề xuất (mỗi lần đề xuất = 1 bước, kể cả bị chặn)
-- ----------------------------------------------------------------------------
CREATE TABLE steps (
    session_id     uuid        NOT NULL,
    step_no        integer     NOT NULL,                 -- trigger cấp: steps_used + 1
    requested_tool text        NOT NULL,                 -- tên LLM đề xuất (có thể ngoài allowlist)
    tool_name      text,                                 -- chỉ có giá trị khi nằm trong allowlist
    arguments      jsonb       NOT NULL DEFAULT '{}'::jsonb,
    rationale      text        NOT NULL DEFAULT '',
    plan_idx       smallint,
    decision       text        NOT NULL DEFAULT 'running',
    detail         text        NOT NULL DEFAULT '',
    started_at     timestamptz NOT NULL DEFAULT clock_timestamp(),
    finished_at    timestamptz,
    duration_ms    integer,
    -- Cột sinh dùng cho khóa ngoại từ evidence: bằng chứng chỉ gắn được vào bước ĐÃ thực thi.
    is_executed    boolean GENERATED ALWAYS AS (decision = 'executed') STORED,
    CONSTRAINT pk_steps PRIMARY KEY (session_id, step_no),
    CONSTRAINT uq_steps_executed_ref UNIQUE (session_id, step_no, is_executed),
    CONSTRAINT fk_steps_session FOREIGN KEY (session_id) REFERENCES agent_sessions (id) ON DELETE RESTRICT,
    CONSTRAINT fk_steps_tool    FOREIGN KEY (tool_name)  REFERENCES allowed_tools (name) ON DELETE RESTRICT,
    CONSTRAINT fk_steps_plan    FOREIGN KEY (session_id, plan_idx) REFERENCES plan_steps (session_id, idx),
    CONSTRAINT ck_steps_step_no        CHECK (step_no BETWEEN 1 AND 20),
    CONSTRAINT ck_steps_requested_tool CHECK (char_length(requested_tool) BETWEEN 1 AND 100),
    CONSTRAINT ck_steps_arguments      CHECK (jsonb_typeof(arguments) = 'object'),
    CONSTRAINT ck_steps_decision       CHECK (decision IN ('running', 'executed', 'tool_error',
                                                           'invalid_arguments', 'duplicate', 'blocked_policy')),
    CONSTRAINT ck_steps_tool_matches   CHECK (tool_name IS NULL OR tool_name = requested_tool),
    -- Bị chặn bởi allowlist <=> không có tool_name (vì tool_name phải nằm trong allowlist)
    CONSTRAINT ck_steps_blocked_no_tool CHECK ((decision = 'blocked_policy') = (tool_name IS NULL)),
    CONSTRAINT ck_steps_finished       CHECK ((decision = 'running') = (finished_at IS NULL)),
    CONSTRAINT ck_steps_duration       CHECK (duration_ms IS NULL OR duration_ms >= 0)
);

-- ----------------------------------------------------------------------------
-- Nhật ký gọi LLM (cơ sở tính token)
-- ----------------------------------------------------------------------------
CREATE TABLE llm_calls (
    session_id    uuid        NOT NULL,
    call_no       integer     NOT NULL,                  -- trigger cấp
    purpose       text        NOT NULL,
    provider      text        NOT NULL,
    model         text        NOT NULL,
    input_tokens  integer     NOT NULL,
    output_tokens integer     NOT NULL,
    total_tokens  integer GENERATED ALWAYS AS (input_tokens + output_tokens) STORED,
    duration_ms   integer     NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_llm_calls PRIMARY KEY (session_id, call_no),
    CONSTRAINT fk_llm_calls_session FOREIGN KEY (session_id) REFERENCES agent_sessions (id) ON DELETE RESTRICT,
    CONSTRAINT ck_llm_calls_purpose  CHECK (purpose IN ('plan', 'act', 'synthesize')),
    CONSTRAINT ck_llm_calls_provider CHECK (char_length(btrim(provider)) BETWEEN 1 AND 50),
    CONSTRAINT ck_llm_calls_model    CHECK (char_length(btrim(model)) BETWEEN 1 AND 100),
    CONSTRAINT ck_llm_calls_tokens   CHECK (input_tokens >= 0 AND output_tokens >= 0),
    CONSTRAINT ck_llm_calls_duration CHECK (duration_ms >= 0)
);

-- ----------------------------------------------------------------------------
-- Bằng chứng (EvidenceStore): append-only, có chuỗi hash chống sửa/xóa
-- ----------------------------------------------------------------------------
CREATE TABLE evidence (
    session_id       uuid        NOT NULL,
    seq              integer     NOT NULL,               -- trigger cấp; hiển thị là E{seq}
    step_no          integer     NOT NULL,
    step_is_executed boolean     NOT NULL DEFAULT true,
    source_uri       text        NOT NULL,
    title            text        NOT NULL,
    content          text        NOT NULL,               -- nội dung đã qua InjectionGuard
    raw_sha256       text        NOT NULL,               -- hash nội dung gốc lấy từ nguồn
    content_sha256   text        NOT NULL,               -- trigger tính từ content
    prev_hash        text        NOT NULL,               -- trigger: chain_hash của bằng chứng liền trước
    chain_hash       text        NOT NULL,               -- trigger: SHA-256(prev | seq | step | uri | raw | content)
    flagged          boolean     NOT NULL DEFAULT false,
    findings         jsonb       NOT NULL DEFAULT '[]'::jsonb,
    retrieved_at     timestamptz NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_evidence PRIMARY KEY (session_id, seq),
    CONSTRAINT fk_evidence_session FOREIGN KEY (session_id) REFERENCES agent_sessions (id) ON DELETE RESTRICT,
    -- (session, step, true) phải tồn tại trong steps => bước tương ứng đã "executed"
    CONSTRAINT fk_evidence_step FOREIGN KEY (session_id, step_no, step_is_executed)
        REFERENCES steps (session_id, step_no, is_executed) ON DELETE RESTRICT,
    CONSTRAINT ck_evidence_step_executed CHECK (step_is_executed),
    CONSTRAINT ck_evidence_seq        CHECK (seq >= 1),
    CONSTRAINT ck_evidence_source_uri CHECK (char_length(source_uri) BETWEEN 1 AND 2000),
    CONSTRAINT ck_evidence_title      CHECK (char_length(btrim(title)) BETWEEN 1 AND 500),
    CONSTRAINT ck_evidence_content    CHECK (char_length(content) BETWEEN 1 AND 20000),
    CONSTRAINT ck_evidence_raw_sha256 CHECK (raw_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT ck_evidence_content_sha256 CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT ck_evidence_prev_hash  CHECK (prev_hash ~ '^[0-9a-f]{64}$'),
    CONSTRAINT ck_evidence_chain_hash CHECK (chain_hash ~ '^[0-9a-f]{64}$'),
    CONSTRAINT ck_evidence_findings   CHECK (jsonb_typeof(findings) = 'array'),
    -- CASE bảo đảm thứ tự đánh giá: không gọi jsonb_array_length trên giá trị không phải mảng.
    CONSTRAINT ck_evidence_flagged_has_findings CHECK (
        CASE WHEN NOT flagged THEN true
             WHEN jsonb_typeof(findings) = 'array' THEN jsonb_array_length(findings) > 0
             ELSE false END
    )
);
CREATE INDEX ix_evidence_step ON evidence (session_id, step_no);

-- ----------------------------------------------------------------------------
-- Báo cáo (ReportSynthesizer): mỗi phiên đúng một báo cáo, bất biến
-- ----------------------------------------------------------------------------
CREATE TABLE reports (
    session_id      uuid        NOT NULL,
    status          text        NOT NULL,                -- complete | partial
    stop_reason     text        NOT NULL,
    generated_by    text        NOT NULL,                -- llm | extractive
    markdown        text        NOT NULL,
    warnings        jsonb       NOT NULL DEFAULT '[]'::jsonb,
    steps_completed integer     NOT NULL,
    steps_planned   integer     NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_reports PRIMARY KEY (session_id),
    CONSTRAINT fk_reports_session FOREIGN KEY (session_id) REFERENCES agent_sessions (id) ON DELETE RESTRICT,
    CONSTRAINT ck_reports_status       CHECK (status IN ('complete', 'partial')),
    CONSTRAINT ck_reports_stop_reason  CHECK (stop_reason IN ('enough_evidence', 'plan_done', 'no_progress',
                                                              'cancelled_by_user',
                                                              'budget_steps', 'budget_tokens', 'budget_seconds',
                                                              'error', 'policy_violations')),
    CONSTRAINT ck_reports_generated_by CHECK (generated_by IN ('llm', 'extractive')),
    CONSTRAINT ck_reports_markdown     CHECK (char_length(btrim(markdown)) BETWEEN 1 AND 100000),
    CONSTRAINT ck_reports_warnings     CHECK (jsonb_typeof(warnings) = 'array'),
    CONSTRAINT ck_reports_steps        CHECK (steps_completed >= 0 AND steps_planned >= 0
                                              AND steps_completed <= steps_planned)
);

-- Các bằng chứng được trích dẫn trong báo cáo; khóa ngoại bảo đảm [E#] không bịa.
CREATE TABLE report_citations (
    session_id uuid    NOT NULL,
    seq        integer NOT NULL,
    CONSTRAINT pk_report_citations PRIMARY KEY (session_id, seq),
    CONSTRAINT fk_report_citations_report   FOREIGN KEY (session_id) REFERENCES reports (session_id) ON DELETE RESTRICT,
    CONSTRAINT fk_report_citations_evidence FOREIGN KEY (session_id, seq) REFERENCES evidence (session_id, seq) ON DELETE RESTRICT
);

COMMENT ON TABLE allowed_tools   IS 'Allowlist công cụ; chỉ chấp nhận access = read_only.';
COMMENT ON TABLE agent_sessions  IS 'Phiên điều phối agent; bộ đếm do trigger duy trì, trạng thái theo máy trạng thái ở 002.';
COMMENT ON TABLE steps           IS 'Mỗi hành động agent đề xuất (kể cả bị chặn) là một bước; tính vào ngân sách.';
COMMENT ON TABLE evidence        IS 'Append-only. UPDATE/DELETE/TRUNCATE bị trigger chặn; chain_hash do CSDL tính.';
COMMENT ON TABLE reports         IS 'Mỗi phiên kết thúc (kể cả bị hủy) bắt buộc có đúng một báo cáo.';

