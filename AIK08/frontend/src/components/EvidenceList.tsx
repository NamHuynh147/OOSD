import { Evidence, Integrity, safeHref } from "../api/client";

export function IntegrityBadge({
  integrity,
  count,
}: {
  integrity: Integrity | null;
  count: number;
}) {
  if (!integrity || count === 0) return null;
  return integrity.ok ? (
    <span
      className="integrity ok"
      title="Chuỗi băm SHA-256 của bằng chứng khớp với CSDL"
    >
      ✓ Chuỗi băm toàn vẹn
    </span>
  ) : (
    <span className="integrity bad">
      ⚠ Chuỗi băm bị phá vỡ: {integrity.broken.map((n) => `E${n}`).join(", ")}
    </span>
  );
}

export function EvidenceList({
  items,
  integrity,
}: {
  items: Evidence[];
  integrity: Integrity | null;
}) {
  return (
    <section className="subpanel">
      <div className="subheading">
        <h4>Bằng chứng</h4>
        <span>{items.length} mục</span>
      </div>
      <IntegrityBadge integrity={integrity} count={items.length} />
      {items.map((e) => {
        const href = safeHref(e.source_uri);
        return (
          <article className="evidence-card" key={e.seq}>
            <div className="evidence-title">
              <span className="evidence-id">E{e.seq}</span>
              <b>{e.title}</b>
              {e.flagged && <span className="warning-tag">Injection?</span>}
            </div>
            {href ? (
              <a href={href} target="_blank" rel="noreferrer noopener">
                {e.source_uri}
              </a>
            ) : (
              <span className="uri">{e.source_uri}</span>
            )}
            <p>{e.content}</p>
            {e.findings?.length > 0 && (
              <small>
                {e.findings
                  .map((f) => `${f.rule_id} · ${f.category}`)
                  .join(" | ")}
              </small>
            )}
          </article>
        );
      })}
      {items.length === 0 && (
        <p className="empty">Chưa có bằng chứng được lưu.</p>
      )}
    </section>
  );
}
