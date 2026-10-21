# -*- coding: utf-8 -*-
"""Nạp cụm sử liệu mẫu vào PostgreSQL rồi MERGE sang Neo4j."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import psycopg
from neo4j import GraphDatabase

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import COMMON_FIELDS, PREFIX, ROOT, TYPE_TABLES, env, postgres_conninfo, wait_ready
from reference_data import load_reference

RELATION_TYPES = {
    "COMMANDED",
    "PARTICIPATED_IN",
    "OPPOSED_IN",
    "TOOK_PLACE_AT",
    "OCCURRED_DURING",
    "EMPLOYED_STRATEGY",
    "LEFT_HERITAGE",
    "SUPPORTS",
}
NODE_PROPS = (
    "canonical_name",
    "verification_status",
    "historical_role_class",
    "group_type",
    "event_type",
    "spatial_category",
    "modern_name",
    "temporal_granularity",
    "artifact_type",
    "concept_category",
    "source_perspective",
    "raw_text",
    "lunar_year_ganzhi",
    "era_year",
    "solar_year_start",
    "solar_year_end",
)


def upsert_row(cur, table: str, fields: tuple[str, ...], row: dict, conflict: str) -> None:
    assignments = ", ".join(
        "%s = EXCLUDED.%s" % (name, name) for name in fields if name != conflict
    )
    cur.execute(
        "INSERT INTO %s (%s) VALUES (%s) ON CONFLICT (%s) DO UPDATE SET %s"
        % (
            table,
            ", ".join(fields),
            ", ".join("%%(%s)s" % name for name in fields),
            conflict,
            assignments,
        ),
        row,
    )


def upsert_postgres(payload: dict) -> None:
    quote = payload["raw_document"]["text"]
    chunk_id = payload["raw_document"]["doc_id"]
    with psycopg.connect(postgres_conninfo()) as conn:
        with conn.cursor() as cur:
            for entity in payload["entities"]:
                entity_type = entity.get("entity_type")
                if entity_type not in TYPE_TABLES:
                    raise SystemExit("Chủ thể không hợp lệ: %s" % entity_type)
                table, type_fields = TYPE_TABLES[entity_type]
                upsert_row(
                    cur,
                    "dim_entities",
                    COMMON_FIELDS,
                    {name: entity.get(name) for name in COMMON_FIELDS},
                    "entity_id",
                )
                subtype_fields = ("entity_id", *type_fields)
                upsert_row(
                    cur,
                    table,
                    subtype_fields,
                    {name: entity.get(name) for name in subtype_fields},
                    "entity_id",
                )
            document = payload["source_document"]
            cur.execute(
                """
                INSERT INTO source_documents (
                    source_id, title, author_compiler, compilation_era, source_perspective,
                    storage_path, doc_status, doc_version
                ) VALUES (
                    %(source_id)s, %(title)s, %(author_compiler)s, %(compilation_era)s,
                    %(source_perspective)s, %(storage_path)s, %(doc_status)s, %(doc_version)s
                )
                ON CONFLICT (source_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    author_compiler = EXCLUDED.author_compiler,
                    compilation_era = EXCLUDED.compilation_era,
                    source_perspective = EXCLUDED.source_perspective,
                    storage_path = EXCLUDED.storage_path,
                    doc_status = EXCLUDED.doc_status,
                    doc_version = EXCLUDED.doc_version
                """,
                document,
            )
            raw = payload["raw_document"]
            cur.execute(
                """
                INSERT INTO raw_documents (doc_id, source_id, text, checksum)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (doc_id) DO UPDATE SET
                    source_id = EXCLUDED.source_id,
                    text = EXCLUDED.text,
                    checksum = EXCLUDED.checksum
                """,
                (
                    raw["doc_id"],
                    raw["source_id"],
                    raw["text"],
                    hashlib.sha256(raw["text"].encode("utf-8")).hexdigest(),
                ),
            )
            for alias in payload["aliases"]:
                cur.execute(
                    """
                    INSERT INTO entity_aliases (entity_id, alias_name, alias_type, source_citation)
                    VALUES (%(entity_id)s, %(alias_name)s, %(alias_type)s, %(source_citation)s)
                    ON CONFLICT (entity_id, alias_name) DO UPDATE SET
                        alias_type = EXCLUDED.alias_type,
                        source_citation = EXCLUDED.source_citation
                    """,
                    alias,
                )
            for relation in payload["relations"]:
                if relation["relation_type"] not in RELATION_TYPES:
                    raise SystemExit("Loại quan hệ không có trong schema: %s" % relation["relation_type"])
                cur.execute(
                    """
                    INSERT INTO entity_relations (
                        head_id, relation_type, tail_id, source_chunk_ids, evidence_count, quote
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (head_id, relation_type, tail_id) DO UPDATE SET
                        source_chunk_ids = EXCLUDED.source_chunk_ids,
                        evidence_count = EXCLUDED.evidence_count,
                        quote = EXCLUDED.quote
                    """,
                    (relation["head_id"], relation["relation_type"], relation["tail_id"], [chunk_id], 1, quote),
                )
            for measurement in payload["measurements"]:
                cur.execute(
                    """
                    DELETE FROM entity_measurements
                    WHERE entity_id = %(entity_id)s AND raw_expression = %(raw_expression)s
                    """,
                    measurement,
                )
                cur.execute(
                    """
                    INSERT INTO entity_measurements (
                        entity_id, raw_expression, quantity_raw, unit_raw, target_type,
                        normalized_value_si, si_unit, conversion_note
                    ) VALUES (
                        %(entity_id)s, %(raw_expression)s, %(quantity_raw)s, %(unit_raw)s,
                        %(target_type)s, %(normalized_value_si)s, %(si_unit)s, %(conversion_note)s
                    )
                    """,
                    measurement,
                )
            for entity_type, (sequence, prefix) in PREFIX.items():
                cur.execute(
                    """
                    SELECT MAX(substring(entity_id FROM %s)::int)
                    FROM dim_entities
                    WHERE entity_type = %s AND entity_id LIKE %s
                    """,
                    (len(prefix) + 1, entity_type, prefix + "%"),
                )
                current = cur.fetchone()[0]
                if current:
                    cur.execute("SELECT setval(%s, %s)", (sequence, current))
        conn.commit()


def merge_graph(payload: dict) -> None:
    quote = payload["raw_document"]["text"]
    chunk_id = payload["raw_document"]["doc_id"]
    aliases = {}
    for alias in payload["aliases"]:
        aliases.setdefault(alias["entity_id"], []).append(alias["alias_name"])
    driver = GraphDatabase.driver(
        "bolt://localhost:%s" % env("NEO4J_BOLT_PORT"),
        auth=(env("NEO4J_USER"), env("NEO4J_PASSWORD")),
    )
    with driver.session() as session:
        for entity in payload["entities"]:
            label = entity["entity_type"]
            if label not in PREFIX:
                raise SystemExit("Chủ thể không hợp lệ: %s" % label)
            props = {name: entity[name] for name in NODE_PROPS if entity.get(name) is not None}
            if entity["entity_id"] in aliases:
                props["aliases"] = aliases[entity["entity_id"]]
            session.run(
                "MERGE (n:%s {id: $id}) SET n += $props" % label,
                id=entity["entity_id"],
                props=props,
            )
        for relation in payload["relations"]:
            session.run(
                """
                MATCH (a {id: $head}), (b {id: $tail})
                MERGE (a)-[r:%s]->(b)
                SET r.source_chunk_ids = $chunks, r.evidence_count = 1, r.quote = $quote
                """
                % relation["relation_type"],
                head=relation["head_id"],
                tail=relation["tail_id"],
                chunks=[chunk_id],
                quote=quote,
            )
    driver.close()


def main() -> None:
    wait_ready()
    load_reference()
    payload = json.loads((ROOT / "data" / "seed.json").read_text(encoding="utf-8"))
    upsert_postgres(payload)
    merge_graph(payload)
    print("Đã nạp seed vào PostgreSQL và Neo4j.")


if __name__ == "__main__":
    main()
