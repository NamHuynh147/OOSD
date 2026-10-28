export type Step = { position: number; goal: string; status: string };
export type Evidence = { id: string; source: string; content: string; flagged: boolean };
export type ResearchSession = {
  id: string;
  question: string;
  status: string;
  steps: Step[];
  evidence: Evidence[];
  report: string | null;
  error: string | null;
  used_steps: number;
  used_tokens: number;
};

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const error = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(error?.detail ?? `Request failed (${response.status})`);
  }
  return (await response.json()) as T;
}

export function createSession(question: string): Promise<ResearchSession> {
  return request("/api/sessions", {
    method: "POST",
    body: JSON.stringify({ question }),
  });
}

export function getSession(id: string): Promise<ResearchSession> {
  return request(`/api/sessions/${encodeURIComponent(id)}`);
}

export function cancelSession(id: string): Promise<ResearchSession> {
  return request(`/api/sessions/${encodeURIComponent(id)}/cancel`, { method: "POST" });
}
