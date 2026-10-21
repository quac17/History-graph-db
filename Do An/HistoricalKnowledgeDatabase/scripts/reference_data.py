# -*- coding: utf-8 -*-
"""Nạp danh mục niên hiệu, can chi và đơn vị đo. Không cấp mã chủ thể."""
from __future__ import annotations

import json

import psycopg

from common import ROOT, postgres_conninfo


def load_reference() -> None:
    payload = json.loads((ROOT / "data" / "init_reference.json").read_text(encoding="utf-8"))
    stems = payload["ganzhi_stems"]
    branches = payload["ganzhi_branches"]
    with psycopg.connect(postgres_conninfo()) as conn:
        with conn.cursor() as cur:
            for item in payload["eras"]:
                cur.execute(
                    """
                    INSERT INTO ref_historical_eras (
                        era_id, dynasty_name, king_name, era_name, start_year_solar, end_year_solar
                    ) VALUES (%(era_id)s, %(dynasty_name)s, %(king_name)s, %(era_name)s,
                              %(start_year_solar)s, %(end_year_solar)s)
                    ON CONFLICT (era_id) DO UPDATE SET
                        dynasty_name = EXCLUDED.dynasty_name,
                        king_name = EXCLUDED.king_name,
                        era_name = EXCLUDED.era_name,
                        start_year_solar = EXCLUDED.start_year_solar,
                        end_year_solar = EXCLUDED.end_year_solar
                    """,
                    item,
                )
            for index in range(60):
                stem = stems[index % 10]
                branch = branches[index % 12]
                cur.execute(
                    """
                    INSERT INTO ref_ganzhi_cycles (ganzhi_name, stem_vi, branch_vi)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (ganzhi_name) DO UPDATE SET
                        stem_vi = EXCLUDED.stem_vi,
                        branch_vi = EXCLUDED.branch_vi
                    """,
                    ("%s %s" % (stem, branch), stem, branch),
                )
            for item in payload["units"]:
                cur.execute(
                    """
                    INSERT INTO ref_measurement_units (
                        unit_id, raw_unit_name, category, si_unit, conversion_factor, historical_context
                    ) VALUES (%(unit_id)s, %(raw_unit_name)s, %(category)s, %(si_unit)s,
                              %(conversion_factor)s, %(historical_context)s)
                    ON CONFLICT (unit_id) DO UPDATE SET
                        raw_unit_name = EXCLUDED.raw_unit_name,
                        category = EXCLUDED.category,
                        si_unit = EXCLUDED.si_unit,
                        conversion_factor = EXCLUDED.conversion_factor,
                        historical_context = EXCLUDED.historical_context
                    """,
                    item,
                )
        conn.commit()
