"""Regression cases captured from real CLI output, reported in issue #1.

These rows are not synthetic templates. They are the exact captures published
in the issue thread, kept separately from the template corpus so that the
model is never fitted to the strings it is evaluated on.
"""
import json
from pathlib import Path

import pytest

from verdict_tiny.model import Verdict

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "real_traces.jsonl"


@pytest.fixture(scope="module")
def model():
    return Verdict(ROOT / "weights" / "verdict-q8.bin")


def _rows() -> list[dict]:
    return [json.loads(line) for line in FIXTURE.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_fixture_is_not_empty():
    assert _rows()


@pytest.mark.parametrize("row", _rows(), ids=lambda row: row["id"])
def test_real_trace_label(model, row):
    result = model.predict(row["command"], row["exit_code"], row.get("stdout", ""), row.get("stderr", ""))
    if row.get("expected") is None:
        assert result["label"] in model.labels
        return
    assert result["label"] == row["expected"], f"{row['id']}: got {result['label']} {result['probabilities']}"
