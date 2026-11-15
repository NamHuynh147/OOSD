import { PlanStep, Step } from "../api/client";

const MARK: Record<string, string> = { done: "✓", skipped: "–" };

export function Progress({ plan, steps }: { plan: PlanStep[]; steps: Step[] }) {
  return (
    <section className="subpanel">
      <div className="subheading">
        <h4>Kế hoạch</h4>
        <span>{plan.length} bước</span>
      </div>
      {plan.map((p) => (
        <div className="plan-row" key={p.idx}>
          <span className={`plan-number ${p.status}`}>
            {MARK[p.status] || String(p.idx).padStart(2, "0")}
          </span>
          <div>
            <b>{p.title}</b>
            <p>{p.goal}</p>
          </div>
          <small>{p.status === "skipped" ? "bỏ qua" : p.status}</small>
        </div>
      ))}
      {steps.length > 0 && (
        <>
          <div className="subheading spaced">
            <h4>Nhật ký thực thi</h4>
          </div>
          {steps.map((s) => (
            <div className="step-row" key={s.step_no}>
              <span className={`step-dot ${s.decision}`} />
              <div>
                <b>
                  #{s.step_no} · {s.requested_tool}
                </b>
                <p>{s.detail || s.decision}</p>
              </div>
              <small>{s.decision}</small>
            </div>
          ))}
        </>
      )}
    </section>
  );
}
