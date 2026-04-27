const BASE = (import.meta.env.VITE_API_BASE_URL as string) || "http://localhost:8000";

export interface EvidenceItem {
  source: string;
  record_id?: string | null;
  description?: string | null;
}

export interface TraceItem {
  node: string;
  detail?: string | null;
  elapsed_ms?: number | null;
  [k: string]: unknown;
}

export interface ChatResponse {
  answer: string;
  intent: string;
  used_sources: string[];
  evidence: EvidenceItem[];
  trace: TraceItem[];
  limitations: string[];
}

export async function postChat(message: string): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) {
    throw new Error(`POST /chat failed: ${res.status}`);
  }
  return (await res.json()) as ChatResponse;
}
