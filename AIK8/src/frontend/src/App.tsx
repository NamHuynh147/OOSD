import { useEffect, useState } from "react";
import { cancelSession, createSession, getSession, type ResearchSession } from "./api/client";
import CancelButton from "./components/CancelButton";
import QueryForm from "./components/QueryForm";
import ReportView from "./components/ReportView";
import StepTimeline from "./components/StepTimeline";

const activeStatuses = new Set(["queued", "running"]);

export default function App() {
  const [session, setSession] = useState<ResearchSession | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const active = session !== null && activeStatuses.has(session.status);

  useEffect(() => {
    if (!session || !active) return;
    const timer = window.setInterval(() => {
      getSession(session.id).then(setSession).catch((cause: Error) => setError(cause.message));
    }, 1200);
    return () => window.clearInterval(timer);
  }, [session?.id, active]);

  async function submit(question: string) {
    setBusy(true);
    setError(null);
    try {
      setSession(await createSession(question));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không thể tạo phiên tra cứu.");
    } finally {
      setBusy(false);
    }
  }

  async function cancel() {
    if (!session) return;
    try {
      setSession(await cancelSession(session.id));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Không thể hủy phiên.");
    }
  }

  return (
    <main className="page">
      <header className="hero">
        <div className="eyebrow">AIK08 · READ-ONLY RESEARCH</div>
        <h1>Tra cứu có kiểm soát</h1>
        <p>Agent chỉ đọc nguồn được cho phép. Mọi kết luận được liên kết tới bằng chứng.</p>
      </header>
      <QueryForm onSubmit={submit} disabled={busy || active} />
      {error && <p className="error" role="alert">{error}</p>}
      {session && (
        <>
          <section className="session-bar">
            <div><span className="muted">Trạng thái</span><strong>{session.status}</strong></div>
            <div><span className="muted">Bước / token ước tính</span><strong>{session.used_steps} · {session.used_tokens}</strong></div>
            {active && <CancelButton onCancel={cancel} disabled={false} />}
          </section>
          {session.error && <p className="error" role="alert">{session.error}</p>}
          <div className="results-grid">
            <StepTimeline steps={session.steps} />
            <ReportView report={session.report} evidence={session.evidence} />
          </div>
        </>
      )}
    </main>
  );
}
