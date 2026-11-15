import { FormEvent, useState } from "react";
import { Session } from "../api/client";
import { Status } from "./Status";

type Props = {
  sessions: Session[];
  selected: string;
  busy: boolean;
  onSelect: (id: string) => void;
  onCreate: (query: string) => Promise<boolean>;
};

export function SessionList({
  sessions,
  selected,
  busy,
  onSelect,
  onCreate,
}: Props) {
  const [query, setQuery] = useState("");
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (query.trim().length < 3) return;
    if (await onCreate(query.trim())) setQuery("");
  }
  return (
    <aside className="panel sidebar">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">WORKSPACE</p>
          <h3>Phiên tra cứu</h3>
        </div>
        <span className="count">{sessions.length}</span>
      </div>
      <form onSubmit={submit} className="new-session">
        <label htmlFor="query">Bạn muốn tra cứu điều gì?</label>
        <textarea
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={4}
          maxLength={2000}
          placeholder="Ví dụ: Tóm tắt quy trình xử lý sự cố và các SLA liên quan…"
        />
        <button className="primary" disabled={busy || query.trim().length < 3}>
          {busy ? "Đang tạo…" : "＋ Tạo phiên tra cứu"}
        </button>
      </form>
      <div className="session-list">
        {sessions.map((s) => (
          <button
            key={s.id}
            className={`session-item ${selected === s.id ? "active" : ""}`}
            onClick={() => onSelect(s.id)}
          >
            <div className="session-item-top">
              <Status status={s.status} />
              <time>
                {s.created_at
                  ? new Date(s.created_at).toLocaleString("vi-VN", {
                      dateStyle: "short",
                      timeStyle: "short",
                    })
                  : ""}
              </time>
            </div>
            <p>{s.query}</p>
            <small>{s.id.slice(0, 8)}…</small>
          </button>
        ))}
        {sessions.length === 0 && (
          <p className="empty">Chưa có phiên. Hãy tạo một yêu cầu ở trên.</p>
        )}
      </div>
    </aside>
  );
}
