import type { Step } from "../api/client";

export default function StepTimeline({ steps }: { steps: Step[] }) {
  return (
    <section className="panel">
      <h2>Tiến trình</h2>
      {steps.length === 0 ? (
        <p className="muted">Đang lập kế hoạch…</p>
      ) : (
        <ol className="timeline">
          {steps.map((step) => (
            <li key={step.position} className={`step step-${step.status}`}>
              <span className="step-marker">{step.status === "done" ? "✓" : step.position}</span>
              <span>{step.goal}</span>
              <small>{step.status}</small>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
