# -*- coding: utf-8 -*-
"""Tạo .env, cài thư viện Python và kiểm tra Docker. Không bật database."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ENV_FILE, ROOT, load_env, run


def main() -> None:
    created = not ENV_FILE.is_file()
    load_env()
    if created:
        print("Đã tạo .env từ .env.example.", flush=True)
    else:
        print(".env đã có, giữ nguyên.", flush=True)
    run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")])
    run(["docker", "compose", "version"])
    print(
        "Đã chuẩn bị xong. Bước sau: yarn init_db, yarn generated_db, yarn reset_db, yarn seed_db.",
        flush=True,
    )


if __name__ == "__main__":
    main()
