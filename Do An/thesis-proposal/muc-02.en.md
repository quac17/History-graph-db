## 2. RESEARCH OVERVIEW

**Problem Statement & Motivation:** The 2018 history curriculum asks learners to state an event with time and place, point to the source, and connect cause with course of events. Classroom 5W1H worksheets stay in the notebook: they cannot be reused, and source fidelity cannot be measured. A digital library can find a book but cannot answer a question inside the file, for example who was present at the Bach Dang battle of 1288. An LLM can answer fluently and still add a year or a person that the source does not contain. One person often has several names, so a store is easy to duplicate. This thesis builds a measurable pipeline: from Vietnamese historical text, through entity records and relations with quotations, to a knowledge graph, with a human-labeled gold set.

**Research Objectives & Questions:** The overall objective is to build and measure a pipeline in which digitized Vietnamese historical text is extracted into entity records and relations, name variants of the same person are merged into one node, and the result is loaded into a knowledge graph.

- O1. Fix the schema of the subject-and-keyword system (eight fixed subjects, keyword sets, opaque identifiers issued by PostgreSQL, closed classifications, relation types) and run three databases with Docker.
- O2. Build four APIs, the pipeline of extraction, entity resolution, and graph ingest, and an operator demo.
- O3. Build a gold set of about 150 to 200 labeled passages, then measure F1 score and precision on the test set.

Research questions:

- RQ1. Where do current ways of managing historical sources and extracting events help or hinder Vietnamese text and school history?
- RQ2. Within the thesis scope, what feasible method extracts entity records and relations, resolves name variants, and loads a graph?
- RQ3. How can extraction quality and entity-resolution quality be measured?

**Scope and Limitations:**

In scope:

- Digitized Vietnamese text.
- A pilot corpus on the resistance against the Mongol-Yuan armies, centered on the Bach Dang battle of 1288.
- Eight fixed subjects: Person, Group, Event, Place, TimeSpan, Artifact, Concept, and Source, together with the agreed relations.
- Neo4j with demo data. PostgreSQL as the master registry: it issues opaque identifiers and stores aliases, sources, and logs. ChromaDB with a schema and a few sample records.
- Four endpoints, `/extract-5w1h`, `/resolve-entity`, `/ingest-graph`, and `/entities/{entity_id}`, and a Streamlit demo.

Out of scope, left for later:

- A student chatbot, ToolPlanner, and classroom trials.
- Bulk chunking and embedding.
- Recording divergent readings between two sources.
- OCR.

How results are recorded in the thesis:

- A keyword or relation without a quotation stays DRAFT and is not presented as checked.
- A match that is not sure enough to merge automatically is FLAGGED.
