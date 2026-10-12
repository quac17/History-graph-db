## 5. RESOURCE REQUIREMENTS & RISK MANAGEMENT

**Required Resources:** A personal machine with enough RAM to run Neo4j and PostgreSQL together. The three databases run with Docker Compose. No separate server is required. The LLM is called through an API. The API key is not committed to the repository. Alias comparison uses a small embedding model and does not require a GPU. Test text comes from textbooks and permitted historical passages. No proprietary dataset is purchased.

**Risk & Mitigation:**

- R1. The model misses an entity or extracts something the text does not say. Mitigation: reject a result that breaks the schema; a missing quotation stays DRAFT.
- R2. Two different people are merged. Mitigation: tune the threshold on the dev set; below the threshold the case is FLAGGED and no new node is created.
- R3. Scope grows into a chatbot. Mitigation: the demo has three steps and no chat box.
- R4. Changing the model mid-way makes the numbers incomparable. Mitigation: every run logs the model name; the final report uses one configuration.
