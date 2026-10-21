# -*- coding: utf-8 -*-
"""Khởi động lại container PostgreSQL và Neo4j. Không xóa volume."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import compose, load_env, run


def main() -> None:
    load_env()
    run(compose("up", "-d", "--force-recreate"))
    print("Đã khởi động PostgreSQL và Neo4j. ChromaDB và agent không chạy ở bước này.")


if __name__ == "__main__":
    main()
