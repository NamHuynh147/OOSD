import { FormEvent, useState } from "react";

type Props = { onSubmit: (question: string) => Promise<void>; disabled: boolean };

export default function QueryForm({ onSubmit, disabled }: Props) {
  const [question, setQuestion] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = question.trim();
    if (value.length < 3) return;
    await onSubmit(value);
  }

  return (
    <form className="query-form" onSubmit={submit}>
      <label htmlFor="question">Bạn muốn tìm hiểu điều gì?</label>
      <textarea
        id="question"
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Ví dụ: Chính sách lưu trữ nhật ký truy cập là gì?"
        maxLength={4000}
        required
        minLength={3}
        disabled={disabled}
      />
      <div className="form-footer">
        <span>Tối đa 4.000 ký tự · Chỉ đọc nguồn được cấp phép</span>
        <button type="submit" disabled={disabled || question.trim().length < 3}>
          Bắt đầu tra cứu
        </button>
      </div>
    </form>
  );
}
