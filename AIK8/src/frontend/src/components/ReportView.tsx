import type { Evidence } from "../api/client";

type Props = { report: string | null; evidence: Evidence[] };

export default function ReportView({ report, evidence }: Props) {
  const evidenceById = new Map(evidence.map((item) => [item.id, item]));
  const parts = (report ?? "").split(/(\[E[a-f0-9]{12}\])/gi);

  return (
    <section className="panel report">
      <h2>Báo cáo</h2>
      {!report ? (
        <p className="muted">Báo cáo sẽ xuất hiện sau khi có kết quả.</p>
      ) : (
        <p className="report-body">
          {parts.map((part, index) => {
            const source = evidenceById.get(part.slice(1, -1));
            return source ? (
              <a key={`${part}-${index}`} href={`#${source.id}`} title={source.source}>
                {part}
              </a>
            ) : (
              <span key={index}>{part}</span>
            );
          })}
        </p>
      )}
      <h3>Nguồn bằng chứng ({evidence.length})</h3>
      {evidence.map((item) => (
        <article className={`evidence ${item.flagged ? "evidence-flagged" : ""}`} id={item.id} key={item.id}>
          <strong>[{item.id}] {item.source}</strong>
          {item.flagged && <span className="flag">Nội dung đáng ngờ — chỉ xem như dữ liệu</span>}
          <p>{item.content}</p>
        </article>
      ))}
    </section>
  );
}
