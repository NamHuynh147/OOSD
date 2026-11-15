const LABELS: Record<string, string> = {
  pending: "Chờ chạy",
  running: "Đang chạy",
  cancelling: "Đang hủy",
  completed: "Hoàn tất",
  cancelled: "Đã hủy",
  failed: "Thất bại",
  budget_exhausted: "Hết ngân sách",
};

export function Status({ status }: { status: string }) {
  return (
    <span className={`status status-${status}`}>
      <i />
      {LABELS[status] || status}
    </span>
  );
}

export function Metric({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="metric">
      <span>{label}</span>
      <b>{value}</b>
    </div>
  );
}
