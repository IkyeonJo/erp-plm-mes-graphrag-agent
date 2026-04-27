import type { TraceItem } from "../lib/api";

interface Props {
  trace: TraceItem[];
}

export default function TraceTimeline({ trace }: Props) {
  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700">Agent Trace</h3>
      {trace.length === 0 ? (
        <p className="mt-2 text-xs text-slate-400">아직 trace가 없습니다.</p>
      ) : (
        <ol className="relative ml-3 mt-3 border-l border-slate-200">
          {trace.map((t, i) => (
            <li key={i} className="ml-4 mb-3">
              <span className="absolute -left-1.5 mt-1 h-3 w-3 rounded-full bg-slate-700" />
              <div className="text-xs font-medium text-slate-700">{t.node}</div>
              <pre className="mt-1 whitespace-pre-wrap break-words rounded bg-slate-50 p-1 font-mono text-[11px] text-slate-500">
                {JSON.stringify(
                  Object.fromEntries(Object.entries(t).filter(([k]) => k !== "node")),
                  null,
                  0,
                )}
              </pre>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
