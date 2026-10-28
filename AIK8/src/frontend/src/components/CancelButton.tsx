export default function CancelButton({
  onCancel,
  disabled,
}: {
  onCancel: () => void;
  disabled: boolean;
}) {
  return (
    <button className="button-secondary" type="button" onClick={onCancel} disabled={disabled}>
      Hủy phiên
    </button>
  );
}
