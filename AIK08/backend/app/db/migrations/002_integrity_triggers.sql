-- ============================================================================
-- 002_integrity_triggers.sql — Ràng buộc nghiệp vụ thực thi ngay trong CSDL
--
-- Mã lỗi riêng (SQLSTATE lớp 'AK'); ứng dụng ánh xạ sang ngoại lệ miền:
--   AK001  budget_exceeded:<steps|tokens|seconds>   hết ngân sách
--   AK002  immutable_*                              sửa/xóa dữ liệu bất biến
--   AK003  invalid_transition / session_not_*       trạng thái không hợp lệ
--   AK004  plan_cardinality                         kế hoạch không có 3–6 bước
--   AK005  unknown_citation / citation_*            trích dẫn [E#] sai
--   AK006  report_required / report_mismatch        phiên kết thúc thiếu/sai báo cáo
--
-- Mọi hàm ghim search_path để không phụ thuộc cấu hình của người gọi.
-- Hàm SECURITY DEFINER chỉ dùng khi phải khóa/cập nhật bảng mà vai trò ứng dụng
-- cố ý KHÔNG có quyền ghi trực tiếp (bộ đếm ngân sách, chuỗi hash).
-- ============================================================================

SET search_path = aik08, pg_catalog;

-- ----------------------------------------------------------------------------
-- R1. Bảng append-only: cấm UPDATE / DELETE / TRUNCATE
-- ----------------------------------------------------------------------------
CREATE FUNCTION trg_forbid_mutation() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
BEGIN
    RAISE EXCEPTION 'immutable_table:%', TG_TABLE_NAME
        USING ERRCODE = 'AK002',
              DETAIL  = format('Thao tác %s bị cấm: bảng %s chỉ cho phép INSERT (append-only).',
                               TG_OP, TG_TABLE_NAME);
END
$$;

-- Bằng chứng, nhật ký LLM, báo cáo, trích dẫn: tuyệt đối bất biến
CREATE TRIGGER trg_evidence_immutable        BEFORE UPDATE OR DELETE ON evidence
    FOR EACH ROW EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_evidence_no_truncate      BEFORE TRUNCATE ON evidence
    FOR EACH STATEMENT EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_llm_calls_immutable       BEFORE UPDATE OR DELETE ON llm_calls
    FOR EACH ROW EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_llm_calls_no_truncate     BEFORE TRUNCATE ON llm_calls
    FOR EACH STATEMENT EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_reports_immutable         BEFORE UPDATE OR DELETE ON reports
    FOR EACH ROW EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_reports_no_truncate       BEFORE TRUNCATE ON reports
    FOR EACH STATEMENT EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_report_citations_immutable BEFORE UPDATE OR DELETE ON report_citations
    FOR EACH ROW EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_report_citations_no_truncate BEFORE TRUNCATE ON report_citations
    FOR EACH STATEMENT EXECUTE FUNCTION trg_forbid_mutation();

-- Phiên / kế hoạch / bước: không bao giờ bị xóa (UPDATE có luật riêng bên dưới)
CREATE TRIGGER trg_sessions_no_delete        BEFORE DELETE ON agent_sessions
    FOR EACH ROW EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_sessions_no_truncate      BEFORE TRUNCATE ON agent_sessions
    FOR EACH STATEMENT EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_plan_steps_no_delete      BEFORE DELETE ON plan_steps
    FOR EACH ROW EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_plan_steps_no_truncate    BEFORE TRUNCATE ON plan_steps
    FOR EACH STATEMENT EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_steps_no_delete           BEFORE DELETE ON steps
    FOR EACH ROW EXECUTE FUNCTION trg_forbid_mutation();
CREATE TRIGGER trg_steps_no_truncate         BEFORE TRUNCATE ON steps
    FOR EACH STATEMENT EXECUTE FUNCTION trg_forbid_mutation();

-- ----------------------------------------------------------------------------
-- R2. Phiên: trạng thái khởi tạo, máy trạng thái, cột bất biến, bộ đếm dẫn xuất
-- ----------------------------------------------------------------------------
CREATE FUNCTION trg_sessions_before_insert() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
BEGIN
    IF NEW.status <> 'pending' OR NEW.steps_used <> 0 OR NEW.tokens_used <> 0
       OR NEW.stop_reason IS NOT NULL OR NEW.started_at IS NOT NULL
       OR NEW.finished_at IS NOT NULL OR NEW.cancel_requested_at IS NOT NULL THEN
        RAISE EXCEPTION 'invalid_initial_state'
            USING ERRCODE = 'AK003',
                  DETAIL  = 'Phiên mới phải ở trạng thái pending với bộ đếm bằng 0.';
    END IF;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_sessions_before_insert BEFORE INSERT ON agent_sessions
    FOR EACH ROW EXECUTE FUNCTION trg_sessions_before_insert();

CREATE FUNCTION trg_sessions_before_update() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    terminal_states constant text[] := ARRAY['completed', 'cancelled', 'budget_exhausted', 'failed'];
    transition_ok   boolean;
BEGIN
    IF NEW.id <> OLD.id OR NEW.query <> OLD.query OR NEW.created_at <> OLD.created_at
       OR NEW.max_steps <> OLD.max_steps OR NEW.max_tokens <> OLD.max_tokens
       OR NEW.max_seconds <> OLD.max_seconds THEN
        RAISE EXCEPTION 'immutable_column:agent_sessions'
            USING ERRCODE = 'AK002',
                  DETAIL  = 'id, query, created_at và các hạn mức max_* là bất biến.';
    END IF;

    -- steps_used / tokens_used chỉ do trigger của steps / llm_calls cập nhật
    -- (khi đó UPDATE này chạy lồng trong trigger khác: pg_trigger_depth() >= 2).
    IF (NEW.steps_used <> OLD.steps_used OR NEW.tokens_used <> OLD.tokens_used)
       AND pg_trigger_depth() < 2 THEN
        RAISE EXCEPTION 'derived_counter:agent_sessions'
            USING ERRCODE = 'AK002',
                  DETAIL  = 'steps_used / tokens_used là cột dẫn xuất, không được ghi trực tiếp.';
    END IF;
    IF NEW.steps_used < OLD.steps_used OR NEW.tokens_used < OLD.tokens_used THEN
        RAISE EXCEPTION 'counter_decrease:agent_sessions'
            USING ERRCODE = 'AK002', DETAIL = 'Bộ đếm ngân sách không được giảm.';
    END IF;

    -- Trạng thái kết thúc là cuối cùng: không cột nào được đổi nữa.
    IF OLD.status = ANY (terminal_states) THEN
        IF ROW(NEW.*) IS DISTINCT FROM ROW(OLD.*) THEN
            RAISE EXCEPTION 'session_finished:%', OLD.status
                USING ERRCODE = 'AK003',
                      DETAIL  = 'Phiên đã kết thúc; không thể thay đổi.';
        END IF;
        RETURN NEW;
    END IF;

    IF NEW.status IS DISTINCT FROM OLD.status THEN
        transition_ok := CASE OLD.status
            WHEN 'pending'    THEN NEW.status = 'running'
            WHEN 'running'    THEN NEW.status IN ('cancelling', 'completed', 'cancelled', 'budget_exhausted', 'failed')
            WHEN 'cancelling' THEN NEW.status IN ('cancelled', 'completed', 'budget_exhausted', 'failed')
            ELSE false
        END;
        IF NOT transition_ok THEN
            RAISE EXCEPTION 'invalid_transition:% -> %', OLD.status, NEW.status
                USING ERRCODE = 'AK003';
        END IF;
        IF NEW.status = 'running' THEN
            NEW.started_at := clock_timestamp();
        END IF;
        IF NEW.status IN ('cancelling', 'cancelled') AND NEW.cancel_requested_at IS NULL THEN
            NEW.cancel_requested_at := clock_timestamp();
        END IF;
        IF NEW.status = ANY (terminal_states) THEN
            NEW.finished_at := clock_timestamp();
        END IF;
    END IF;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_sessions_before_update BEFORE UPDATE ON agent_sessions
    FOR EACH ROW EXECUTE FUNCTION trg_sessions_before_update();

-- Quy tắc cốt lõi của cơ chế hủy phiên: kết thúc (kể cả bị hủy) => PHẢI có báo cáo,
-- phần đã có được trả về. Kiểm tra lúc COMMIT nên ứng dụng chèn báo cáo và đổi trạng
-- thái trong cùng một giao dịch.
CREATE FUNCTION trg_sessions_report_required() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    r reports%ROWTYPE;
BEGIN
    SELECT * INTO r FROM reports WHERE session_id = NEW.id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'report_required:%', NEW.status
            USING ERRCODE = 'AK006',
                  DETAIL  = 'Phiên kết thúc (kể cả bị hủy) phải có báo cáo; trả về phần đã có.';
    END IF;
    IF r.stop_reason IS DISTINCT FROM NEW.stop_reason
       OR r.status IS DISTINCT FROM (CASE WHEN NEW.status = 'completed' THEN 'complete' ELSE 'partial' END) THEN
        RAISE EXCEPTION 'report_mismatch:%', NEW.id
            USING ERRCODE = 'AK006',
                  DETAIL  = 'Báo cáo phải complete khi phiên completed, partial trong mọi trường hợp khác; stop_reason phải khớp.';
    END IF;
    RETURN NULL;
END
$$;
CREATE CONSTRAINT TRIGGER ctrg_sessions_report_required
    AFTER UPDATE OF status ON agent_sessions
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW
    WHEN (NEW.status IN ('completed', 'cancelled', 'budget_exhausted', 'failed'))
    EXECUTE FUNCTION trg_sessions_report_required();

-- ----------------------------------------------------------------------------
-- R3. Kế hoạch: chỉ tạo một lần, bằng MỘT câu INSERT, gồm 3–6 bước đánh số liên tục
-- ----------------------------------------------------------------------------
CREATE FUNCTION trg_plan_steps_before_insert() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    s text;
BEGIN
    SELECT status INTO s FROM agent_sessions WHERE id = NEW.session_id;
    IF s IS DISTINCT FROM 'running' THEN
        RAISE EXCEPTION 'session_not_running:%', COALESCE(s, 'unknown')
            USING ERRCODE = 'AK003', DETAIL = 'Chỉ lập kế hoạch khi phiên đang chạy.';
    END IF;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_plan_steps_before_insert BEFORE INSERT ON plan_steps
    FOR EACH ROW EXECUTE FUNCTION trg_plan_steps_before_insert();

CREATE FUNCTION trg_plan_steps_before_update() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
BEGIN
    IF NEW.session_id <> OLD.session_id OR NEW.idx <> OLD.idx OR NEW.title <> OLD.title
       OR NEW.goal <> OLD.goal OR NEW.tool_hint IS DISTINCT FROM OLD.tool_hint THEN
        RAISE EXCEPTION 'immutable_column:plan_steps' USING ERRCODE = 'AK002',
              DETAIL = 'Chỉ cột status của bước kế hoạch được cập nhật.';
    END IF;
    IF OLD.status <> 'pending' AND NEW.status <> OLD.status THEN
        RAISE EXCEPTION 'invalid_transition:% -> %', OLD.status, NEW.status USING ERRCODE = 'AK003';
    END IF;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_plan_steps_before_update BEFORE UPDATE ON plan_steps
    FOR EACH ROW EXECUTE FUNCTION trg_plan_steps_before_update();

-- Trigger mức câu lệnh với bảng chuyển tiếp: thấy toàn bộ các dòng của câu INSERT.
CREATE FUNCTION trg_plan_steps_cardinality() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    r record;
BEGIN
    FOR r IN
        SELECT n.session_id,
               count(*)   AS inserted,
               max(n.idx) AS max_idx,
               (SELECT count(*) FROM plan_steps p WHERE p.session_id = n.session_id) AS total
        FROM new_rows n
        GROUP BY n.session_id
    LOOP
        IF r.total <> r.inserted THEN
            RAISE EXCEPTION 'plan_already_exists:%', r.session_id
                USING ERRCODE = 'AK004', DETAIL = 'Mỗi phiên chỉ có một kế hoạch, tạo bằng một câu INSERT.';
        END IF;
        IF r.inserted NOT BETWEEN 3 AND 6 OR r.max_idx <> r.inserted THEN
            RAISE EXCEPTION 'plan_cardinality:%', r.inserted
                USING ERRCODE = 'AK004',
                      DETAIL  = format('Kế hoạch phải có 3–6 bước đánh số liên tục từ 1; nhận %s bước (idx lớn nhất %s).',
                                       r.inserted, r.max_idx);
        END IF;
    END LOOP;
    RETURN NULL;
END
$$;
CREATE TRIGGER trg_plan_steps_cardinality AFTER INSERT ON plan_steps
    REFERENCING NEW TABLE AS new_rows
    FOR EACH STATEMENT EXECUTE FUNCTION trg_plan_steps_cardinality();

-- ----------------------------------------------------------------------------
-- R4. Bước: ngân sách (bước · token · giây) chặn NGAY TẠI CSDL, bộ đếm do trigger giữ
-- ----------------------------------------------------------------------------
CREATE FUNCTION trg_steps_before_insert() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    s agent_sessions%ROWTYPE;
BEGIN
    SELECT * INTO s FROM agent_sessions WHERE id = NEW.session_id FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'unknown_session:%', NEW.session_id USING ERRCODE = '23503';
    END IF;
    IF s.status <> 'running' THEN
        RAISE EXCEPTION 'session_not_running:%', s.status
            USING ERRCODE = 'AK003', DETAIL = 'Chỉ thêm bước khi phiên đang chạy (không phải đang hủy/đã kết thúc).';
    END IF;
    IF s.steps_used >= s.max_steps THEN
        RAISE EXCEPTION 'budget_exceeded:steps' USING ERRCODE = 'AK001',
              DETAIL = format('Đã dùng %s/%s bước.', s.steps_used, s.max_steps);
    END IF;
    IF s.tokens_used >= s.max_tokens THEN
        RAISE EXCEPTION 'budget_exceeded:tokens' USING ERRCODE = 'AK001',
              DETAIL = format('Đã dùng %s/%s token.', s.tokens_used, s.max_tokens);
    END IF;
    IF clock_timestamp() > s.started_at + make_interval(secs => s.max_seconds) THEN
        RAISE EXCEPTION 'budget_exceeded:seconds' USING ERRCODE = 'AK001',
              DETAIL = format('Đã quá hạn %s giây kể từ khi phiên bắt đầu.', s.max_seconds);
    END IF;

    NEW.step_no := s.steps_used + 1;
    IF NEW.decision <> 'running' THEN
        NEW.finished_at := clock_timestamp();
        NEW.duration_ms := GREATEST(0, round(extract(epoch FROM (NEW.finished_at - NEW.started_at)) * 1000))::integer;
    END IF;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_steps_before_insert BEFORE INSERT ON steps
    FOR EACH ROW EXECUTE FUNCTION trg_steps_before_insert();

CREATE FUNCTION trg_steps_after_insert() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = aik08, pg_catalog, pg_temp
AS $$
BEGIN
    UPDATE agent_sessions SET steps_used = steps_used + 1 WHERE id = NEW.session_id;
    RETURN NULL;
END
$$;
CREATE TRIGGER trg_steps_after_insert AFTER INSERT ON steps
    FOR EACH ROW EXECUTE FUNCTION trg_steps_after_insert();

-- Một bước chỉ đổi được một lần: running -> executed | tool_error; các cột khác bất biến.
CREATE FUNCTION trg_steps_before_update() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
BEGIN
    IF OLD.decision <> 'running' THEN
        RAISE EXCEPTION 'immutable_row:steps' USING ERRCODE = 'AK002',
              DETAIL = 'Bước đã hoàn tất không được sửa.';
    END IF;
    IF NEW.decision NOT IN ('executed', 'tool_error') THEN
        RAISE EXCEPTION 'invalid_transition:% -> %', OLD.decision, NEW.decision USING ERRCODE = 'AK003';
    END IF;
    IF NEW.session_id <> OLD.session_id OR NEW.step_no <> OLD.step_no
       OR NEW.requested_tool <> OLD.requested_tool OR NEW.tool_name IS DISTINCT FROM OLD.tool_name
       OR NEW.arguments <> OLD.arguments OR NEW.rationale <> OLD.rationale
       OR NEW.plan_idx IS DISTINCT FROM OLD.plan_idx OR NEW.started_at <> OLD.started_at THEN
        RAISE EXCEPTION 'immutable_column:steps' USING ERRCODE = 'AK002',
              DETAIL = 'Chỉ decision và detail của bước đang chạy được cập nhật.';
    END IF;
    NEW.finished_at := clock_timestamp();
    NEW.duration_ms := GREATEST(0, round(extract(epoch FROM (NEW.finished_at - OLD.started_at)) * 1000))::integer;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_steps_before_update BEFORE UPDATE ON steps
    FOR EACH ROW EXECUTE FUNCTION trg_steps_before_update();

-- ----------------------------------------------------------------------------
-- R5. Nhật ký LLM: cộng dồn token vào phiên (cột dẫn xuất)
-- ----------------------------------------------------------------------------
CREATE FUNCTION trg_llm_calls_before_insert() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    s agent_sessions%ROWTYPE;
BEGIN
    SELECT * INTO s FROM agent_sessions WHERE id = NEW.session_id FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'unknown_session:%', NEW.session_id USING ERRCODE = '23503';
    END IF;
    IF s.status NOT IN ('running', 'cancelling') THEN
        RAISE EXCEPTION 'session_not_active:%', s.status USING ERRCODE = 'AK003';
    END IF;
    SELECT COALESCE(max(call_no), 0) + 1 INTO NEW.call_no FROM llm_calls WHERE session_id = NEW.session_id;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_llm_calls_before_insert BEFORE INSERT ON llm_calls
    FOR EACH ROW EXECUTE FUNCTION trg_llm_calls_before_insert();

CREATE FUNCTION trg_llm_calls_after_insert() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = aik08, pg_catalog, pg_temp
AS $$
BEGIN
    UPDATE agent_sessions
       SET tokens_used = tokens_used + NEW.input_tokens + NEW.output_tokens
     WHERE id = NEW.session_id;
    RETURN NULL;
END
$$;
CREATE TRIGGER trg_llm_calls_after_insert AFTER INSERT ON llm_calls
    FOR EACH ROW EXECUTE FUNCTION trg_llm_calls_after_insert();

-- ----------------------------------------------------------------------------
-- R6. Bằng chứng: số thứ tự E#, chuỗi hash do CSDL tính (ứng dụng không giả mạo được)
-- ----------------------------------------------------------------------------
CREATE FUNCTION evidence_chain_hash(p_prev text, p_seq integer, p_step_no integer,
                                    p_uri text, p_raw text, p_content_sha text) RETURNS text
LANGUAGE sql IMMUTABLE PARALLEL SAFE
SET search_path = pg_catalog
AS $$
    SELECT encode(sha256(convert_to(
        p_prev || '|' || p_seq::text || '|' || p_step_no::text || '|' || p_uri || '|' || p_raw || '|' || p_content_sha,
        'UTF8')), 'hex')
$$;

CREATE FUNCTION trg_evidence_before_insert() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    s         agent_sessions%ROWTYPE;
    last_seq  integer;
    last_hash text;
BEGIN
    SELECT * INTO s FROM agent_sessions WHERE id = NEW.session_id FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'unknown_session:%', NEW.session_id USING ERRCODE = '23503';
    END IF;
    -- 'cancelling' vẫn được ghi: kết quả công cụ đang dở khi người dùng hủy là "phần đã có".
    IF s.status NOT IN ('running', 'cancelling') THEN
        RAISE EXCEPTION 'session_not_active:%', s.status USING ERRCODE = 'AK003';
    END IF;

    SELECT e.seq, e.chain_hash INTO last_seq, last_hash
      FROM evidence e WHERE e.session_id = NEW.session_id
     ORDER BY e.seq DESC LIMIT 1;

    NEW.seq            := COALESCE(last_seq, 0) + 1;
    NEW.prev_hash      := COALESCE(last_hash, repeat('0', 64));
    NEW.content_sha256 := encode(sha256(convert_to(NEW.content, 'UTF8')), 'hex');
    NEW.chain_hash     := evidence_chain_hash(NEW.prev_hash, NEW.seq, NEW.step_no, NEW.source_uri,
                                              NEW.raw_sha256, NEW.content_sha256);
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_evidence_before_insert BEFORE INSERT ON evidence
    FOR EACH ROW EXECUTE FUNCTION trg_evidence_before_insert();

-- Kiểm tra toàn vẹn chuỗi: tính lại hash theo thứ tự; ok = false nếu dữ liệu bị can thiệp
-- (ví dụ superuser tắt trigger rồi sửa trực tiếp).
CREATE FUNCTION verify_evidence_chain(p_session uuid)
RETURNS TABLE (seq integer, ok boolean, reason text)
LANGUAGE sql STABLE
SET search_path = aik08, pg_catalog, pg_temp
AS $$
    WITH ordered AS (
        SELECT e.*,
               lag(e.chain_hash) OVER (ORDER BY e.seq) AS expected_prev,
               row_number()      OVER (ORDER BY e.seq) AS rn
          FROM evidence e
         WHERE e.session_id = p_session
    )
    SELECT o.seq,
           (o.seq = o.rn
            AND o.prev_hash = COALESCE(o.expected_prev, repeat('0', 64))
            AND o.content_sha256 = encode(sha256(convert_to(o.content, 'UTF8')), 'hex')
            AND o.chain_hash = evidence_chain_hash(o.prev_hash, o.seq, o.step_no, o.source_uri,
                                                   o.raw_sha256, o.content_sha256)) AS ok,
           CASE
               WHEN o.seq <> o.rn THEN 'seq_gap'
               WHEN o.prev_hash <> COALESCE(o.expected_prev, repeat('0', 64)) THEN 'prev_hash_mismatch'
               WHEN o.content_sha256 <> encode(sha256(convert_to(o.content, 'UTF8')), 'hex') THEN 'content_modified'
               WHEN o.chain_hash <> evidence_chain_hash(o.prev_hash, o.seq, o.step_no, o.source_uri,
                                                        o.raw_sha256, o.content_sha256) THEN 'chain_hash_mismatch'
               ELSE 'ok'
           END AS reason
      FROM ordered o
     ORDER BY o.seq
$$;

-- ----------------------------------------------------------------------------
-- R7. Báo cáo: trích dẫn [E#] phải có thật; bảng trích dẫn khớp văn bản;
--     số bước kế hoạch khớp dữ liệu; có bằng chứng thì phải có trích dẫn
-- ----------------------------------------------------------------------------
CREATE FUNCTION trg_reports_before_insert() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    s text;
    n integer;
BEGIN
    SELECT status INTO s FROM agent_sessions WHERE id = NEW.session_id;
    IF s IS NULL OR s NOT IN ('running', 'cancelling') THEN
        RAISE EXCEPTION 'session_not_active:%', COALESCE(s, 'unknown')
            USING ERRCODE = 'AK003',
                  DETAIL  = 'Báo cáo được ghi khi phiên đang chạy hoặc đang hủy, trước khi chuyển sang trạng thái kết thúc.';
    END IF;
    FOR n IN
        SELECT DISTINCT (m[1])::integer FROM regexp_matches(NEW.markdown, '\[E([0-9]{1,6})\]', 'g') AS m
    LOOP
        IF NOT EXISTS (SELECT 1 FROM evidence WHERE session_id = NEW.session_id AND seq = n) THEN
            RAISE EXCEPTION 'unknown_citation:E%', n
                USING ERRCODE = 'AK005', DETAIL = 'Báo cáo trích dẫn bằng chứng không tồn tại.';
        END IF;
    END LOOP;
    RETURN NEW;
END
$$;
CREATE TRIGGER trg_reports_before_insert BEFORE INSERT ON reports
    FOR EACH ROW EXECUTE FUNCTION trg_reports_before_insert();

CREATE FUNCTION trg_reports_consistent() RETURNS trigger
LANGUAGE plpgsql
SET search_path = aik08, pg_catalog, pg_temp
AS $$
DECLARE
    in_text  integer[];
    in_table integer[];
    n_evid   integer;
    planned  integer;
    done     integer;
BEGIN
    SELECT COALESCE(array_agg(t.n ORDER BY t.n), '{}') INTO in_text
      FROM (SELECT DISTINCT (m[1])::integer AS n
              FROM regexp_matches(NEW.markdown, '\[E([0-9]{1,6})\]', 'g') AS m) t;
    SELECT COALESCE(array_agg(c.seq ORDER BY c.seq), '{}') INTO in_table
      FROM report_citations c WHERE c.session_id = NEW.session_id;
    SELECT count(*) INTO n_evid FROM evidence WHERE session_id = NEW.session_id;

    IF in_text IS DISTINCT FROM in_table THEN
        RAISE EXCEPTION 'citation_mismatch:%', NEW.session_id
            USING ERRCODE = 'AK005',
                  DETAIL  = format('[E#] trong văn bản %s khác bảng report_citations %s.', in_text, in_table);
    END IF;
    IF n_evid > 0 AND cardinality(in_table) = 0 THEN
        RAISE EXCEPTION 'citation_required:%', NEW.session_id
            USING ERRCODE = 'AK005',
                  DETAIL  = format('Phiên có %s bằng chứng nhưng báo cáo không trích dẫn bằng chứng nào.', n_evid);
    END IF;

    SELECT count(*), count(*) FILTER (WHERE status = 'done') INTO planned, done
      FROM plan_steps WHERE session_id = NEW.session_id;
    IF NEW.steps_planned <> planned OR NEW.steps_completed <> done THEN
        RAISE EXCEPTION 'report_progress_mismatch:%', NEW.session_id
            USING ERRCODE = 'AK006',
                  DETAIL  = format('Báo cáo ghi %s/%s bước nhưng kế hoạch có %s/%s.',
                                   NEW.steps_completed, NEW.steps_planned, done, planned);
    END IF;
    RETURN NULL;
END
$$;
CREATE CONSTRAINT TRIGGER ctrg_reports_consistent
    AFTER INSERT ON reports
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION trg_reports_consistent();
