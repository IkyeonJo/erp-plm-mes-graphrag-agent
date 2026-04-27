import type { ChatResponse } from "../lib/api";

interface Props {
  response: ChatResponse | null;
  loading: boolean;
  error: string | null;
  demoQuestions: string[];
  onSelectDemo: (q: string) => void;
}

export default function ChatWindow({
  response,
  loading,
  error,
  demoQuestions,
  onSelectDemo,
}: Props) {
  return (
    <div className="rounded-lg border bg-white p-5 shadow-sm">
      <div className="mb-3">
        <h2 className="text-sm font-semibold text-slate-700">데모 질문</h2>
        <div className="mt-2 flex flex-wrap gap-2">
          {demoQuestions.map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => onSelectDemo(q)}
              className="rounded border border-slate-200 bg-slate-50 px-3 py-1 text-xs text-slate-600 hover:bg-slate-100"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      <hr className="my-4" />

      {loading && (
        <div className="rounded bg-slate-50 p-4 text-sm text-slate-500">
          Supervisor Agent 실행 중...
        </div>
      )}

      {error && (
        <div className="rounded bg-red-50 p-4 text-sm text-red-700">
          오류: {error}
        </div>
      )}

      {response && (
        <div className="space-y-3">
          <div>
            <span className="rounded bg-slate-800 px-2 py-1 text-xs text-white">
              {response.intent}
            </span>
            <span className="ml-2 text-xs text-slate-500">
              sources: {response.used_sources.join(", ") || "—"}
            </span>
          </div>
          <article className="whitespace-pre-wrap text-sm leading-relaxed text-slate-800">
            {response.answer}
          </article>
          {response.limitations?.length > 0 && (
            <div className="rounded bg-amber-50 p-3 text-xs text-amber-800">
              <div className="font-semibold">Limitations</div>
              <ul className="ml-4 list-disc">
                {response.limitations.map((l, i) => (
                  <li key={i}>{l}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {!loading && !response && !error && (
        <div className="rounded bg-slate-50 p-4 text-sm text-slate-500">
          질문을 입력하거나, 위의 데모 질문을 선택하세요.
        </div>
      )}
    </div>
  );
}
