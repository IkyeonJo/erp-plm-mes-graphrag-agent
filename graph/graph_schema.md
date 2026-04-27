# Neo4j Graph Schema

자세한 설계는 [`docs/06_knowledge_graph_schema.md`](../docs/06_knowledge_graph_schema.md) 참고.

## 파일

| 파일 | 용도 |
|---|---|
| `cypher/01_schema.cypher` | 라벨/관계 가이드 + 인덱스 |
| `cypher/02_constraints.cypher` | 핵심 ID Uniqueness |
| `cypher/03_load_data.cypher` | synthetic CSV 적재 (`LOAD CSV WITH HEADERS`) |
| `cypher/04_sample_queries.cypher` | 5개 Use Case에 매핑되는 GraphRAG 질의 |

## 적재 절차 (Docker Compose)

1. `docker compose up neo4j -d`
2. `data/synthetic` 을 Neo4j import 디렉터리(`/var/lib/neo4j/import`)에 마운트
   (PoC에서는 Python loader 권장: `backend/scripts/load_graph.py` 추가 가능)
3. Neo4j Browser([http://localhost:7474](http://localhost:7474))에서 차례로 실행
   - `:source 02_constraints.cypher`
   - `:source 03_load_data.cypher`
4. 샘플 질의 검증
   - `:source 04_sample_queries.cypher`

## PoC 단순화

- 본 MVP에서는 `LOAD CSV` 대신 **Python loader** 사용을 권장한다 (Neo4j import dir 마운트 이슈 회피).
- Python loader는 `backend/scripts/load_graph.py` 에 추후 추가하며, 동일한 MERGE 구조를 따른다.
