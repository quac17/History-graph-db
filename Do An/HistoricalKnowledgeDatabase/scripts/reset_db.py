# -*- coding: utf-8 -*-
"""Xóa dữ liệu, tạo lại schema và nạp danh mục. Không nạp seed sử liệu."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import apply_schema, compose, env, run, wait_ready
from reference_data import load_reference


def main() -> None:
    wait_ready()
    run(
        compose(
            "exec", "-T", "postgres",
            "psql", "-v", "ON_ERROR_STOP=1",
            "-U", env("POSTGRES_USER"),
            "-d", env("POSTGRES_DB"),
        ),
        "DROP SCHEMA public CASCADE;\nCREATE SCHEMA public;\n",
    )
    run(
        compose(
            "exec", "-T", "neo4j",
            "cypher-shell",
            "-u", env("NEO4J_USER"),
            "-p", env("NEO4J_PASSWORD"),
        ),
        "MATCH (n) DETACH DELETE n;\n",
    )
    apply_schema()
    load_reference()
    print("Đã tạo lại bảng, ràng buộc và danh mục. Chưa nạp seed sử liệu.")


if __name__ == "__main__":
    main()
