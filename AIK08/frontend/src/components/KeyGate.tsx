import { FormEvent, useState } from "react";

type Props = { rejected: boolean; onSave: (key: string) => void };

export function KeyGate({ rejected, onSave }: Props) {
  const [key, setKey] = useState("");
  function submit(event: FormEvent) {
    event.preventDefault();
    if (key.trim()) onSave(key);
  }
  return (
    <section className="panel key-gate" aria-labelledby="key-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">XÁC THỰC</p>
          <h3 id="key-title">Nhập API key</h3>
        </div>
      </div>
      <form onSubmit={submit} className="new-session">
        <label htmlFor="api-key">
          API key của máy chủ (một trong các khóa trong <code>API_KEYS</code>)
        </label>
        <input
          id="api-key"
          type="password"
          autoComplete="off"
          value={key}
          onChange={(e) => setKey(e.target.value)}
        />
        {rejected && (
          <div className="error-banner key-error" role="alert">
            Khóa không đúng hoặc đã bị thu hồi.
          </div>
        )}
        <button className="primary" disabled={!key.trim()}>
          Lưu và tiếp tục
        </button>
        <small className="key-note">
          Khóa chỉ giữ trong tab này (sessionStorage) và gửi qua header
          X-API-Key.
        </small>
      </form>
    </section>
  );
}
