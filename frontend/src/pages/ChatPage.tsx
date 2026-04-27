import { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import EvidencePanel from "../components/EvidencePanel";
import TraceTimeline from "../components/TraceTimeline";
import GraphResultPanel from "../components/GraphResultPanel";
import { postChat, type ChatResponse } from "../lib/api";

const DEMO_QUESTIONS = [
  "A제품의 최근 3개월 불량률이 상승한 원인을 분석해줘.",
  "공급사 S-03의 부품이 들어간 제품과 최근 품질 이슈를 요약해줘.",
  "최근 설계변경이 있었던 제품 중 불량률이 증가한 제품을 찾아줘.",
  "PLM BOM과 MES 실제 투입 부품이 다른 LOT를 찾아줘.",
  "A제품의 BOM, 재고, 생산실적, 불량률을 통합 요약해줘.",
];

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [resp, setResp] = useState<ChatResponse | null>(null);
  const [err, setErr] = useState<string | null>(null);

  async function handleSend(message: string) {
    if (!message.trim()) return;
    setLoading(true);
    setErr(null);
    try {
      const data = await postChat(message);
      setResp(data);
    } catch (e) {
      setErr((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto grid max-w-6xl gap-6 px-6 py-6 lg:grid-cols-3">
      <section className="lg:col-span-2 space-y-4">
        <ChatWindow
          response={resp}
          loading={loading}
          error={err}
          onSelectDemo={(q) => {
            setInput(q);
            handleSend(q);
          }}
          demoQuestions={DEMO_QUESTIONS}
        />

        <form
          className="flex gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            handleSend(input);
          }}
        >
          <input
            className="flex-1 rounded border border-slate-300 bg-white px-4 py-2 text-sm focus:border-slate-500 focus:outline-none"
            placeholder="질문을 입력하세요 (예: A제품 불량 원인 분석)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            className="rounded bg-slate-800 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "분석 중..." : "전송"}
          </button>
        </form>
      </section>

      <aside className="space-y-4">
        <EvidencePanel evidence={resp?.evidence ?? []} sources={resp?.used_sources ?? []} />
        <GraphResultPanel
          path={resp?.evidence?.find((e) => e.source === "Neo4j")?.description ?? null}
        />
        <TraceTimeline trace={resp?.trace ?? []} />
      </aside>
    </div>
  );
}
