## 2. RESEARCH OVERVIEW

**Problem Statement & Motivation:** The 2018 history curriculum asks learners to state an event with time and place, point to the source, and connect cause with course of events. In class, a history lesson stays in the notebook: it is hard to reuse, and source fidelity cannot be measured. A digital library can find a book but cannot answer a question inside the file, for example who was present at the Bach Dang battle of 1288. An LLM can answer fluently and still add a year or a person that the source does not contain. One person often has several names, so a store is easy to duplicate. Practice therefore needs a system that addresses these problems.

**Research Objectives & Questions:** The overall objective of the thesis is a measurable pipeline:

- From Vietnamese historical text, to entity records whose relations are established by extracting knowledge from the source passage with an LLM, to a knowledge graph that records the relations among those entities.
- A sample gold set labeled by people.

- O1. Fix the schema of the subject-and-keyword system (eight fixed subjects, keyword sets, opaque identifiers issued by PostgreSQL, closed classifications, relation types) and run three databases with Docker.
- O2. Build the APIs and the pipeline for extraction, entity resolution, and graph ingest, together with an operator demo.
- O3. Build a gold set of about 150 to 200 passages labeled by people, then measure F1 score and the precision of data extraction on the test set.

Research questions:

- RQ1. Where do current ways of managing historical sources and extracting events help or hinder Vietnamese text and school history?
- RQ2. Within the thesis scope, what feasible method extracts entity records and relations, resolves name variants, and loads a graph?
- RQ3. How can extraction quality and entity-resolution quality be measured?

**Novelty and Contributions:** The thesis contributes an entity-based way of storing historical material, and a source-grounded extraction pipeline.

Storage:

- Store by entity rather than by book file.
- One entity has one identifier in the database. Several names still refer to that one entity.
- When several passages concern the same entity, each passage is kept intact with its own source, rather than merged into one text.

Extraction pipeline:

- Store only what the source states, together with the original sentence.
- Passages about the same entity are recognized and gathered under one identifier.
- Two sources are not mixed into one sentence. This avoids treating an AI hallucination as stored fact.

**Scope and Limitations:**

In scope:

- The input is Vietnamese historical text.
- The pilot corpus is labeled material about one historical event, taken from several sources.
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
