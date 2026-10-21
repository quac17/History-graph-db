# -*- coding: utf-8 -*-
"""Tạo schema nếu chưa có. Không xóa dữ liệu đang có."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import apply_schema, wait_ready


def main() -> None:
    wait_ready()
    apply_schema()
    print("Đã áp schema PostgreSQL và ràng buộc Neo4j.")


if __name__ == "__main__":
    main()
