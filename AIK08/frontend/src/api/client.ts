export type Limits = {
  max_steps: number;
  max_tokens: number;
  max_seconds: number;
};
export type Session = {
  id: string;
  query: string;
  status: string;
  stop_reason?: string | null;
  limits?: Limits;
  usage?: { steps: number; tokens: number; seconds: number };
  created_at?: string;
};
export type Finding = { rule_id: string; severity: string; category: string };
export type Evidence = {
  seq: number;
  title: string;
  source_uri: string;
  content: string;
  flagged: boolean;
  findings: Finding[];
};
export type Integrity = { ok: boolean; broken: number[] };
export type Report = {
  status: string;
  stop_reason: string;
  generated_by: string;
  markdown: string;
  citations: number[];
  warnings: string[];
  steps_completed: number;
  steps_planned: number;
};
export type PlanStep = {
  idx: number;
  title: string;
  goal: string;
  status: string;
};
export type Step = {
  step_no: number;
  requested_tool: string;
  decision: string;
  detail: string;
};
export type Detail = {
  session: Session;
  plan: PlanStep[];
  steps: Step[];
  report: Report | null;
};

const API = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");
export const TERMINAL = [
  "completed",
  "cancelled",
  "failed",
  "budget_exhausted",
];
export const isTerminal = (status: string) => TERMINAL.includes(status);

/** FastAPI trả `detail` là chuỗi (lỗi nghiệp vụ) hoặc mảng đối tượng (lỗi 422 kiểm tra dữ liệu). */
export function readableError(detail: unknown, fallback: string): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    const parts = detail.map((d) => {
      if (d && typeof d === "object" && "msg" in d) {
        const loc = Array.isArray((d as { loc?: unknown[] }).loc)
          ? (d as { loc: unknown[] }).loc.filter((x) => x !== "body").join(".")
          : "";
        return loc
          ? `${loc}: ${String((d as { msg: unknown }).msg)}`
          : String((d as { msg: unknown }).msg);
      }
      return String(d);
    });
    if (parts.length) return parts.join("; ");
  }
  return fallback;
}

/** Khóa API chỉ giữ trong sessionStorage của tab (đóng tab là mất); không nhúng vào bản build. */
const KEY_STORE = "aik08.apiKey";
export function getApiKey(): string {
  try {
    return sessionStorage.getItem(KEY_STORE) || "";
  } catch {
    return "";
  }
}
export function setApiKey(key: string): void {
  try {
    if (key) sessionStorage.setItem(KEY_STORE, key);
    else sessionStorage.removeItem(KEY_STORE);
  } catch {
    /* bộ nhớ bị chặn: bỏ qua */
  }
}
export class UnauthorizedError extends Error {
  constructor() {
    super("Cần API key hợp lệ");
    this.name = "UnauthorizedError";
  }
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const key = getApiKey();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(key ? { "X-API-Key": key } : {}),
    ...((init?.headers as Record<string, string>) || {}),
  };
  const response = await fetch(`${API}${path}`, { ...init, headers });
  if (response.status === 401) throw new UnauthorizedError();
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(
      readableError(
        (body as { detail?: unknown }).detail,
        `HTTP ${response.status}`,
      ),
    );
  }
  return response.json() as Promise<T>;
}

export const api = {
  listSessions: () => request<Session[]>("/api/sessions?limit=50"),
  createSession: (query: string) =>
    request<{ session: Session }>("/api/sessions", {
      method: "POST",
      body: JSON.stringify({ query }),
    }),
  getSession: (id: string) => request<Detail>(`/api/sessions/${id}`),
  getEvidence: (id: string) =>
    request<{ items: Evidence[]; integrity: Integrity }>(
      `/api/sessions/${id}/evidence`,
    ),
  cancel: (id: string) =>
    request<Session>(`/api/sessions/${id}/cancel`, { method: "POST" }),
};

/** Chỉ http(s) mới được làm liên kết bấm được; doc://, javascript:, data: ... chỉ hiển thị dạng chữ. */
export function safeHref(uri: string): string | null {
  try {
    const url = new URL(uri);
    return url.protocol === "http:" || url.protocol === "https:"
      ? url.href
      : null;
  } catch {
    return null;
  }
}
