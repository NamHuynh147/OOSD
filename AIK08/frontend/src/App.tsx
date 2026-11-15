import { useCallback, useEffect, useRef, useState } from "react";
import {
  Detail,
  Evidence,
  Integrity,
  Session,
  UnauthorizedError,
  api,
  isTerminal,
  setApiKey,
} from "./api/client";
import { EvidenceList } from "./components/EvidenceList";
import { KeyGate } from "./components/KeyGate";
import { Progress } from "./components/Progress";
import { ReportCard } from "./components/ReportCard";
import { SessionList } from "./components/SessionList";
import { Metric, Status } from "./components/Status";
import { ThemeToggle } from "./components/ThemeToggle";
import "./aik08-theme.css";

function sessionStorageHasKey(): boolean {
  try {
    return Boolean(sessionStorage.getItem("aik08.apiKey"));
  } catch {
    return false;
  }
}

const message = (e: unknown, fallback: string) =>
  e instanceof Error ? e.message : fallback;

function App() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selected, setSelected] = useState("");
  const [detail, setDetail] = useState<Detail | null>(null);
  const [evidence, setEvidence] = useState<Evidence[]>([]);
  const [integrity, setIntegrity] = useState<Integrity | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [cancelling, setCancelling] = useState(false);
  const [needKey, setNeedKey] = useState(false);
  const [keyRejected, setKeyRejected] = useState(false);
  const [draft, setDraft] = useState("");
  const selectedRef = useRef("");
  selectedRef.current = selected;

  // 401: dừng polling và hỏi khóa; các lỗi khác hiện ở banner.
  const fail = useCallback((e: unknown, fallback: string) => {
    if (e instanceof UnauthorizedError) {
      setNeedKey(true);
      return;
    }
    setError(message(e, fallback));
  }, []);

  const refreshSessions = useCallback(async () => {
    try {
      setSessions(await api.listSessions());
      setError("");
      setNeedKey(false);
    } catch (e) {
      fail(e, "Không kết nối được API");
    }
  }, [fail]);

  const refreshSelected = useCallback(
    async (id: string) => {
      try {
        const [d, ev] = await Promise.all([
          api.getSession(id),
          api.getEvidence(id),
        ]);
        if (selectedRef.current !== id) return;
        setDetail(d);
        setEvidence(ev.items || []);
        setIntegrity(ev.integrity);
      } catch (e) {
        fail(e, "Không tải được chi tiết phiên");
      }
    },
    [fail],
  );

  // Danh sách: chỉ poll khi còn phiên chưa kết thúc.
  const anyActive =
    sessions.length === 0 || sessions.some((s) => !isTerminal(s.status));

  useEffect(() => {
    if (needKey) return;
    void refreshSessions();
    if (!anyActive) return;
    const timer = window.setInterval(() => void refreshSessions(), 3000);
    return () => window.clearInterval(timer);
  }, [refreshSessions, anyActive, needKey]);

  // Chi tiết: poll đến khi phiên kết thúc.
  const selectedStatus =
    detail && detail.session.id === selected ? detail.session.status : "";

  useEffect(() => {
    if (!selected || needKey) return;
    void refreshSelected(selected);
    if (selectedStatus && isTerminal(selectedStatus)) return;
    const timer = window.setInterval(
      () => void refreshSelected(selected),
      1800,
    );
    return () => window.clearInterval(timer);
  }, [selected, selectedStatus, refreshSelected, needKey]);

  function select(id: string) {
    setSelected(id);
    setDetail(null);
    setEvidence([]);
    setIntegrity(null);
    setError("");
  }

  async function create(query: string): Promise<boolean> {
    setBusy(true);
    setError("");
    try {
      const result = await api.createSession(query);
      select(result.session.id);
      await refreshSessions();
      return true;
    } catch (e) {
      fail(e, "Không tạo được phiên");
      return false;
    } finally {
      setBusy(false);
    }
  }

  async function submitDraft() {
    const query = draft.trim();
    if (!query || busy) return;

    const created = await create(query);
    if (created) setDraft("");
  }

  async function cancel() {
    if (!selected) return;
    setCancelling(true);
    try {
      await api.cancel(selected);
      await Promise.all([refreshSelected(selected), refreshSessions()]);
    } catch (e) {
      fail(e, "Không hủy được phiên");
    } finally {
      setCancelling(false);
    }
  }

  function saveKey(key: string) {
    setApiKey(key.trim());
    setKeyRejected(false);
    setError("");
    setNeedKey(false);
  }

  // Nếu khóa vừa nhập vẫn bị 401 thì báo trạng thái sai khóa.
  useEffect(() => {
    if (!needKey) return;
    setKeyRejected(Boolean(sessionStorageHasKey()));
  }, [needKey]);

  const status = detail?.session.status ?? "";
  const canCancel = status === "pending" || status === "running";
  const limits = detail?.session.limits;
  const steps = detail?.session.usage?.steps ?? detail?.steps.length ?? 0;

  return (
    <main className="shell app-shell">
      <header className="topbar">
        <div className="brand-mark">OOSD</div>
        <div className="brand-copy">
          <p className="eyebrow">AIK-08 </p>
          <h1>Research Assistant</h1>
        </div>
        <span className="readonly">
          <span /> READ-ONLY
        </span>
        <ThemeToggle />
      </header>

      {needKey ? (
        <KeyGate rejected={keyRejected} onSave={saveKey} />
      ) : (
        <section className="workspace chat-workspace">
          <SessionList
            sessions={sessions}
            selected={selected}
            busy={busy}
            onSelect={select}
            onCreate={create}
          />

          <section className="panel detail-panel chat-main">
            <header className="panel-heading chat-toolbar">
              <div>
                <p className="eyebrow">RESEARCH WORKSPACE</p>
                <h3>
                  {detail
                    ? "Cuộc hội thoại"
                    : selected
                      ? "Đang tải phiên..."
                      : "Trợ lý nghiên cứu"}
                </h3>
              </div>

              <div className="chat-toolbar-actions">
                {detail && <Status status={status} />}
                {detail && (canCancel || status === "cancelling") && (
                  <button
                    className="secondary"
                    onClick={cancel}
                    disabled={cancelling || status === "cancelling"}
                  >
                    {status === "cancelling" ? "Đang hủy…" : "Hủy phiên"}
                  </button>
                )}
              </div>
            </header>

            <div className="chat-scroll">
              {error && (
                <div className="error-banner" role="alert">
                  {error}
                </div>
              )}

              {!detail ? (
                <div className="welcome-state">
                  <div className="welcome-icon">✳</div>
                  <p className="eyebrow">AIK-08 · READ-ONLY RESEARCH AGENT</p>
                  <h2>
                    Bạn muốn <span>tra cứu</span> điều gì?
                  </h2>
                  <p className="welcome-copy">
                    Đặt câu hỏi để Agent lập kế hoạch, tìm kiếm nguồn được cho
                    phép, lưu bằng chứng và tổng hợp báo cáo có trích dẫn.
                  </p>
                  {selected ? (
                    <div className="loading-hint">
                      Đang tải dữ liệu phiên...
                    </div>
                  ) : (
                    <div className="welcome-points">
                      <div>
                        <b>01</b>
                        <span>Allowlist công cụ</span>
                      </div>
                      <div>
                        <b>02</b>
                        <span>Giới hạn ngân sách</span>
                      </div>
                      <div>
                        <b>03</b>
                        <span>Evidence append-only</span>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="conversation">
                  <article className="query-card user-message">
                    <div className="query-card-head">
                      <span className="message-author">Bạn</span>
                      <Status status={status} />
                    </div>
                    <h4>{detail.session.query}</h4>
                    <div className="message-meta">
                      <span className="mono">
                        SESSION · {detail.session.id}
                      </span>
                    </div>
                    <div className="metrics">
                      <Metric
                        label="Bước"
                        value={
                          limits ? `${steps} / ${limits.max_steps}` : steps
                        }
                      />
                      <Metric
                        label="Token"
                        value={`${(detail.session.usage?.tokens ?? 0).toLocaleString("vi-VN")}${limits ? ` / ${limits.max_tokens.toLocaleString("vi-VN")}` : ""}`}
                      />
                      <Metric label="Bằng chứng" value={evidence.length} />
                    </div>
                  </article>

                  <div className="assistant-section">
                    <div className="assistant-heading">
                      <div className="assistant-avatar">AI1</div>
                      <div>
                        <strong>Research Agent</strong>
                        <span>Tiến trình thực hiện</span>
                      </div>
                    </div>

                    <div className="content-grid">
                      <Progress plan={detail.plan} steps={detail.steps} />
                      <EvidenceList items={evidence} integrity={integrity} />
                    </div>

                    {detail.report && (
                      <div className="assistant-report">
                        <div className="assistant-heading">
                          <div className="assistant-avatar">AI2</div>
                          <div>
                            <strong>Báo cáo nghiên cứu</strong>
                            <span>Kết quả tổng hợp từ bằng chứng</span>
                          </div>
                        </div>
                        <ReportCard report={detail.report} />
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            <form
              className="chat-composer-wrap"
              onSubmit={(event) => {
                event.preventDefault();
                void submitDraft();
              }}
            >
              <div className="chat-composer">
                <textarea
                  rows={1}
                  value={draft}
                  onChange={(event) => setDraft(event.target.value)}
                  onKeyDown={(event) => {
                    if (
                      event.key === "Enter" &&
                      !event.shiftKey &&
                      !event.nativeEvent.isComposing
                    ) {
                      event.preventDefault();
                      void submitDraft();
                    }
                  }}
                  placeholder="Nhập câu hỏi hoặc chủ đề cần nghiên cứu..."
                  aria-label="Nhập câu hỏi nghiên cứu"
                  disabled={busy}
                />
                <button
                  className="composer-submit"
                  type="submit"
                  disabled={!draft.trim() || busy}
                  aria-label="Gửi truy vấn"
                  title="Gửi truy vấn"
                >
                  {busy ? "…" : "↑"}
                </button>
              </div>
              <p className="composer-note">
                Enter để gửi · Shift + Enter để xuống dòng · Agent chỉ đọc dữ
                liệu
              </p>
            </form>
          </section>
        </section>
      )}

      <footer className="app-footer">
        <span>AIK-08</span>
        <span>READ-ONLY · TRA CỨU CÓ BẰNG CHỨNG</span>
      </footer>
    </main>
  );
}

export default App;
