"""Golden test for the sprint-report skill: the numbers must never drift."""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "sprint-report"


def run(*args: str) -> dict:
    out = subprocess.run(
        [sys.executable, str(SKILL / "sprint_stats.py"), *args],
        check=True, capture_output=True, text=True,
    )
    return json.loads(out.stdout)


def test_sample_sprint_numbers():
    stats = run(str(SKILL / "fixtures" / "sample-export.csv"))
    assert stats["sprint"] == "Sprint 14"
    assert (stats["committed_points"], stats["completed_points"]) == (19, 10)
    assert stats["completion_pct"] == 53
    assert (stats["bugs_opened"], stats["bugs_closed"]) == (2, 1)
    assert [i["key"] for i in stats["blocked"]] == ["APP-105"]
    assert [i["key"] for i in stats["carry_over"]] == ["APP-104", "APP-105", "APP-106"]


def test_missing_column_fails_loudly(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("Issue key,Summary\nAPP-1,x\n", encoding="utf-8")
    out = subprocess.run(
        [sys.executable, str(SKILL / "sprint_stats.py"), str(bad)],
        capture_output=True, text=True,
    )
    assert out.returncode != 0
    assert "missing columns" in out.stderr
