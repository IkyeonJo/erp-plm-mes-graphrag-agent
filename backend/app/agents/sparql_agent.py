from __future__ import annotations

from app.agents.state import AgentState
from app.tools.sparql_tool import sparql_query

DEFAULT_SPARQL = """
PREFIX : <http://example.org/manufacturing#>
SELECT ?product ?part WHERE {
  ?product a :Product .
  ?product :hasPart ?part .
} LIMIT 20
"""


def call_sparql_agent(state: AgentState) -> AgentState:
    if "SPARQL" not in state.get("required_sources", []):
        return state

    rows = sparql_query(DEFAULT_SPARQL)
    state["sparql_result"] = {"rows": rows, "query": DEFAULT_SPARQL.strip()}
    if rows:
        state["evidence"].append(
            {
                "source": "Ontology.SPARQL",
                "record_id": "sparql-default",
                "description": f"{len(rows)} rows from manufacturing.ttl",
            }
        )
    state["trace"].append({"node": "call_sparql_agent", "rows": len(rows)})
    return state
