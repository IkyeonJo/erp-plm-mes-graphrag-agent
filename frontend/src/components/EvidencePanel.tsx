import type { EvidenceItem } from "../lib/api";

interface Props {
  evidence: EvidenceItem[];
  sources: string[];
}

export default function EvidencePanel({ evidence, sources }: Props) {
  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700">Evidence</h3>
      <p className="mt-1 text-xs text-slate-500">
        Used sources: {sources.length ? sources.join(" / ") : "—"}
      </p>

      <ul className="mt-3 space-y-2 text-xs">
        {evidence.length === 0 ? (
          <li className="text-slate-400">아직 evidence가 없습니다.</li>
        ) : (
          evidence.map((e, i) => (
            <li key={i} className="rounded border border-slate-200 bg-slate-50 p-2">
              <div className="font-mono text-[11px] text-slate-500">{e.source}</div>
              <div className="font-medium text-slate-700">
                {e.record_id ?? "(no record_id)"}
              </div>
              <div className="text-slate-600">{e.description}</div>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
