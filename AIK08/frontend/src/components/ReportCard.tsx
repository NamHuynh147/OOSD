import { Report } from "../api/client";
import { Markdown } from "./Markdown";

const STATE: Record<string, string> = {
  complete: "Hoàn tất",
  partial: "Một phần",
};

export function ReportCard({ report }: { report: Report }) {
  return (
    <section className="report-card">
      <div className="subheading">
        <div>
          <p className="eyebrow">
            FINAL OUTPUT · {report.generated_by.toUpperCase()}
          </p>
          <h4>Báo cáo tra cứu</h4>
        </div>
        <span className={`report-state ${report.status}`}>
          {STATE[report.status] || report.status}
        </span>
      </div>
      <div className="markdown-report">
        <Markdown source={report.markdown} />
      </div>
      {report.warnings?.length > 0 && (
        <div className="warning-box">
          <b>Lưu ý</b>
          {report.warnings.map((w, i) => (
            <p key={i}>{w}</p>
          ))}
        </div>
      )}
    </section>
  );
}
