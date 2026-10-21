# -*- coding: utf-8 -*-
"""Đường dẫn, biến môi trường và kết nối dùng chung cho các lệnh database."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _utf8_stdio() -> None:
    """PowerShell mặc định cp1252; các lệnh in tiếng Việt cần UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


_utf8_stdio()

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"

PREFIX = {
    "Person": ("seq_person", "P"),
    "Event": ("seq_event", "EV"),
    "Group": ("seq_group", "GRP"),
    "Place": ("seq_place", "LOC"),
    "TimeSpan": ("seq_time", "TIM"),
    "Artifact": ("seq_artifact", "ART"),
    "Concept": ("seq_concept", "CON"),
    "Source": ("seq_source", "SRC"),
}

COMMON_FIELDS = (
    "entity_id",
    "entity_type",
    "canonical_name",
    "wikidata_id",
    "verification_status",
    "confidence_score",
)

TYPE_TABLES = {
    "Person": (
        "entity_persons",
        ("historical_role_class", "birth_year", "death_year"),
    ),
    "Group": ("entity_groups", ("group_type",)),
    "Event": ("entity_events", ("event_type",)),
    "Place": ("entity_places", ("spatial_category", "modern_name")),
    "TimeSpan": (
        "entity_timespans",
        (
            "temporal_granularity",
            "raw_text",
            "lunar_day",
            "lunar_month",
            "lunar_year_ganzhi",
            "era_id",
            "era_year",
            "solar_year_start",
            "solar_year_end",
            "solar_date_iso_start",
            "solar_date_iso_end",
        ),
    ),
    "Artifact": ("entity_artifacts", ("artifact_type",)),
    "Concept": ("entity_concepts", ("concept_category",)),
    "Source": ("entity_sources", ("source_perspective",)),
}


def load_env() -> None:
    if not ENV_FILE.is_file():
        shutil.copyfile(ENV_EXAMPLE, ENV_FILE)
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def env(name: str) -> str:
    load_env()
    value = os.environ.get(name)
    if not value:
        raise SystemExit("Thiếu biến %s trong %s" % (name, ENV_FILE))
    return value


def run(args: list[str], input_text: str | None = None) -> None:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        input=input_text,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit("Lệnh thất bại (%s): %s" % (completed.returncode, " ".join(args)))


def compose(*args: str) -> list[str]:
    return ["docker", "compose", "--env-file", str(ENV_FILE), *args]


def postgres_conninfo() -> str:
    return (
        "host=localhost port=%s dbname=%s user=%s password=%s"
        % (env("POSTGRES_PORT"), env("POSTGRES_DB"), env("POSTGRES_USER"), env("POSTGRES_PASSWORD"))
    )


def wait_ready() -> None:
    import psycopg
    from neo4j import GraphDatabase

    last_error = "chưa kết nối được"
    for _ in range(30):
        try:
            with psycopg.connect(postgres_conninfo(), connect_timeout=3) as conn:
                conn.execute("SELECT 1")
            driver = GraphDatabase.driver(
                "bolt://localhost:%s" % env("NEO4J_BOLT_PORT"),
                auth=(env("NEO4J_USER"), env("NEO4J_PASSWORD")),
            )
            driver.verify_connectivity()
            driver.close()
            return
        except Exception as exc:  # noqa: BLE001 - báo lỗi cuối cho người chạy
            last_error = str(exc)
            time.sleep(2)
    raise SystemExit("Database chưa sẵn sàng. Chạy yarn init_db trước.\n%s" % last_error)


def apply_sql_file(path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    run(
        compose(
            "exec", "-T", "postgres",
            "psql", "-v", "ON_ERROR_STOP=1",
            "-U", env("POSTGRES_USER"),
            "-d", env("POSTGRES_DB"),
        ),
        sql,
    )


def apply_cypher_file(path: Path) -> None:
    cypher = path.read_text(encoding="utf-8")
    run(
        compose(
            "exec", "-T", "neo4j",
            "cypher-shell",
            "-u", env("NEO4J_USER"),
            "-p", env("NEO4J_PASSWORD"),
        ),
        cypher,
    )


def apply_schema() -> None:
    apply_sql_file(ROOT / "sql" / "001_schema.sql")
    apply_cypher_file(ROOT / "cypher" / "001_constraints.cypher")
