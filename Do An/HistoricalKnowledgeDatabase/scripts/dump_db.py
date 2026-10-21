# -*- coding: utf-8 -*-
"""Ghi bản dump PostgreSQL và Cypher của graph vào thư mục dumps."""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from neo4j import GraphDatabase

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, compose, env, wait_ready


def cypher_value(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(cypher_value(item) for item in value) + "]"
    text = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return "'%s'" % text


def dump_graph(path: Path) -> None:
    driver = GraphDatabase.driver(
        "bolt://localhost:%s" % env("NEO4J_BOLT_PORT"),
        auth=(env("NEO4J_USER"), env("NEO4J_PASSWORD")),
    )
    lines = []
    with driver.session() as session:
        nodes = session.run(
            """
            MATCH (n)
            RETURN labels(n) AS labels, properties(n) AS props
            ORDER BY n.id
            """
        )
        for record in nodes:
            label = record["labels"][0]
            props = dict(record["props"])
            node_id = props.pop("id")
            assignments = ", ".join("%s: %s" % (key, cypher_value(val)) for key, val in sorted(props.items()))
            if assignments:
                lines.append("MERGE (n:%s {id: %s}) SET n += {%s};" % (label, cypher_value(node_id), assignments))
            else:
                lines.append("MERGE (n:%s {id: %s});" % (label, cypher_value(node_id)))
        relations = session.run(
            """
            MATCH (a)-[r]->(b)
            RETURN a.id AS head, type(r) AS rel_type, b.id AS tail, properties(r) AS props
            ORDER BY head, rel_type, tail
            """
        )
        for record in relations:
            props = dict(record["props"])
            assignments = ", ".join("%s: %s" % (key, cypher_value(val)) for key, val in sorted(props.items()))
            set_clause = " SET r += {%s}" % assignments if assignments else ""
            lines.append(
                "MATCH (a {id: %s}), (b {id: %s}) MERGE (a)-[r:%s]->(b)%s;"
                % (cypher_value(record["head"]), cypher_value(record["tail"]), record["rel_type"], set_clause)
            )
    driver.close()
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    wait_ready()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "dumps"
    out_dir.mkdir(exist_ok=True)
    sql_path = out_dir / ("postgres-%s.sql" % stamp)
    with sql_path.open("w", encoding="utf-8", newline="\n") as handle:
        completed = __import__("subprocess").run(
            compose(
                "exec", "-T", "postgres",
                "pg_dump", "--no-owner", "--no-privileges",
                "-U", env("POSTGRES_USER"),
                "-d", env("POSTGRES_DB"),
            ),
            cwd=ROOT,
            stdout=handle,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    if completed.returncode != 0:
        raise SystemExit("pg_dump thất bại")
    graph_path = out_dir / ("neo4j-%s.cypher" % stamp)
    dump_graph(graph_path)
    print(sql_path)
    print(graph_path)


if __name__ == "__main__":
    main()
