# tasks/04‑sql‑reasoning/python/test_queries.py
import csv
import sqlite3
from pathlib import Path

import queries


# ---------- helpers ------------------------------------------------------- #
_EXPECTED_DIR = Path(__file__).resolve().parent.parent / "expected"


def _fetch(sql: str):
    """Run `sql` against donations.db and return (header, rows_as_strings)."""
    with sqlite3.connect(queries.DB_PATH) as conn:
        cur = conn.execute(sql)
        header = [c[0] for c in cur.description]
        rows = [tuple(str(v) for v in r) for r in cur.fetchall()]

    return header, rows


def _load_expected(csv_name: str):
    path = _EXPECTED_DIR / csv_name
    with path.open(newline="") as fh:
        rdr = csv.reader(fh)
        header = next(rdr)
        rows = [tuple(r) for r in rdr]
    return header, rows


# ---------- tests --------------------------------------------------------- #
def test_task_a_matches_expected():
    exp_h, exp_r = _load_expected("q1.csv")
    got_h, got_r = _fetch(queries.SQL_A)
    assert got_h == exp_h
    assert got_r == exp_r


def test_task_b_matches_expected():
    exp_h, exp_r = _load_expected("q2.csv")
    got_h, got_r = _fetch(queries.SQL_B)
    assert got_h == exp_h
    assert got_r == exp_r
