interface Row {
  [key: string]: unknown;
}

interface Props {
  title: string;
  rows: Row[];
}

export default function SQLResultTable({ title, rows }: Props) {
  if (!rows?.length) {
    return null;
  }

  const headers = Object.keys(rows[0]);
  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
      <div className="mt-3 overflow-x-auto">
        <table className="min-w-full text-xs">
          <thead className="bg-slate-100 text-slate-600">
            <tr>
              {headers.map((h) => (
                <th key={h} className="border px-2 py-1 text-left">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 50).map((r, i) => (
              <tr key={i} className="odd:bg-white even:bg-slate-50">
                {headers.map((h) => (
                  <td key={h} className="border px-2 py-1 text-slate-700">
                    {String(r[h] ?? "")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
