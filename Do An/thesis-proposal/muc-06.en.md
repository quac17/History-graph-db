## 6. 12-WEEK EXECUTION TIMELINE (3 MONTHS)

| Week | Phase | Planned Tasks & Activities | Weekly Milestone / Output |
| --- | --- | --- | --- |
| Week 1 | Preparation | Fix the proposal, set up Git, read background material, sketch the subject-and-keyword system | A working repository and a proposal sent to the supervisor |
| Week 2 | Design | Schema of eight subjects, opaque identifiers, closed classifications, relation types, master registry tables in PostgreSQL | Architecture sketch and a draft Pydantic schema |
| Week 3 | Baseline | Docker Compose for Neo4j, PostgreSQL, and ChromaDB; load one sample record that matches the schema | Three databases running; the sequence issues an identifier; a sample record in Neo4j |
| Week 4 | Core development | API `/extract-5w1h`; start gold-set labeling | The extraction endpoint is callable |
| Week 5 | Core development | `/resolve-entity`, `/ingest-graph`, `/entities/{entity_id}`; continue labeling | Four callable endpoints; a draft API document |
| Week 6 | Midterm | Freeze the schema and classifications at demo level; review the gold set; midterm meeting with the supervisor | Midterm report; schema frozen for measurement |
| Week 7 | Integration | Extraction pipeline, then graph load with MERGE; check source and lifespan constraints | One passage becomes nodes and edges; a reload does not duplicate them |
| Week 8 | Optimization | Automatic entity resolution on the master registry; tighten DRAFT and FLAGGED | An alias already in the master registry resolves to the existing identifier, with no second node |
| Week 9 | Evaluation | Streamlit demo; measure F1 score and precision on the test set | A metrics table; a three-step demo runs |
| Week 10 | Writing | Draft thesis chapters 1, 2, and 3 | Draft of the first half of the thesis |
| Week 11 | Writing | Draft thesis chapters 4, 5, and 6; format to the template | A full draft sent to the supervisor |
| Week 12 | Finalization | Revise from feedback, finish the slides, run a mock defense | Thesis and slides submitted |
