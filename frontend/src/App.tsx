import ChatPage from "./pages/ChatPage";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-6xl px-6 py-4">
          <h1 className="text-xl font-bold text-slate-800">
            ERP/PLM/MES GraphRAG Agent
          </h1>
          <p className="text-sm text-slate-500">
            Synthetic dataset 기반 PoC — FastAPI · LangGraph · Neo4j · RDF/SPARQL
          </p>
        </div>
      </header>
      <main className="flex-1">
        <ChatPage />
      </main>
      <footer className="border-t bg-white text-xs text-slate-400">
        <div className="mx-auto max-w-6xl px-6 py-3">
          PoC for portfolio. All data is synthetic.
        </div>
      </footer>
    </div>
  );
}
