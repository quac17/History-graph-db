## 3. PROPOSED METHODOLOGY

**Core Approach:** The working backend name is HistoryDistill, one monolith application. The processing flow runs in the following order.

- Step 1. The operator imports a file of historical passages.
- Step 2. The system returns a JSON file with two schema-valid lists: the entity records mentioned in the passage, and the relations among them. Every filled keyword and every relation must carry a quotation and a character offset. A result that breaks the schema is rejected.
- Step 3. PostgreSQL issues an opaque identifier for each record.
- Step 4. Person, Group, and Place records pass through entity resolution. The system looks up the alias table in PostgreSQL with a trigram index.
- Step 5. If the match is not sure, it measures string similarity, with a starting threshold of about 80% tuned on the dev set, then compares contextual embeddings. Below the threshold the case is FLAGGED and no new node is created.
- Step 6. Confirmed results are loaded into Neo4j with MERGE on the issued identifier. The same identifier updates the existing node and does not create a second one.
- Step 7. The demo only has to show that an alias already in the master registry resolves to the existing identifier.

**Data & Technologies:** The test corpus is textbook passages or permitted historical passages on the resistance against the Mongol-Yuan armies and the Bach Dang campaign of 1288. The gold set is labeled by a person for subjects, keywords, and relations, without looking at model output. It is split into a dev set and a test set.

Technologies used in the thesis:

- Python, FastAPI, Pydantic.
- Neo4j, PostgreSQL, ChromaDB.
- An LLM with structured output.
- A Vietnamese embedding model (PhoBERT or equivalent), used only to rank aliases.
- Streamlit, Docker Compose, Git.

**Evaluation Plan:** The figures below are targets, not measured results.

| Metric | How it is computed | Target |
| --- | --- | --- |
| Keyword F1 score | Compare each keyword of each entity record with the gold set; a value must have the correct quotation; report each subject | 85% to 90% |
| Relation F1 score | Correct head identifier, relation type, tail identifier, and quotation | 75% to 85% |
| Precision of entity resolution | Only cases the system decides by itself | 90% to 95% |
| Extraction time | From receiving the text to a schema-valid result | Under 3 to 5 seconds per page |

FLAGGED cases are not in the precision denominator. A record without a quotation stays DRAFT. If F1 score is below the target, the report is still valid when it includes an error table by subject and relation type.
