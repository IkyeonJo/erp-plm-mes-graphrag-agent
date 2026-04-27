interface Props {
  path: string | null;
}

export default function GraphResultPanel({ path }: Props) {
  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700">Knowledge Graph</h3>
      {path ? (
        <p className="mt-2 break-words rounded bg-slate-50 p-2 font-mono text-xs text-slate-600">
          {path}
        </p>
      ) : (
        <p className="mt-2 text-xs text-slate-400">
          그래프 결과가 아직 없습니다. 관계/영향/추적 등 graph 키워드가 포함된 질문을 시도해보세요.
        </p>
      )}
    </div>
  );
}
