"""Deterministic sprint numbers from a Jira CSV export. The model never does this arithmetic."""
import argparse
import csv
import json
import sys

DONE = {"done", "closed", "resolved"}
BLOCKED = {"blocked"}
REQUIRED = ["Issue key", "Summary", "Issue Type", "Status", "Sprint"]


def points(row):
    raw = (row.get("Story Points") or row.get("Custom field (Story Points)") or "").strip()
    try:
        return float(raw)
    except ValueError:
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--sprint")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    missing = [c for c in REQUIRED if rows and c not in rows[0]]
    if not rows or missing:
        sys.exit(f"CSV is empty or missing columns: {missing}")

    sprints = [r["Sprint"] for r in rows if r["Sprint"]]
    sprint = args.sprint or sprints[-1]
    in_sprint = [r for r in rows if r["Sprint"] == sprint]
    done = [r for r in in_sprint if r["Status"].lower() in DONE]
    open_ = [r for r in in_sprint if r["Status"].lower() not in DONE]
    bugs = [r for r in in_sprint if r["Issue Type"].lower() == "bug"]

    committed = sum(points(r) for r in in_sprint)
    completed = sum(points(r) for r in done)
    brief = lambda r: {"key": r["Issue key"], "summary": r["Summary"], "status": r["Status"]}
    json.dump({
        "sprint": sprint,
        "committed_issues": len(in_sprint),
        "committed_points": round(committed),
        "completed_issues": len(done),
        "completed_points": round(completed),
        "completion_pct": round(100 * completed / committed) if committed else 0,
        "bugs_opened": len(bugs),
        "bugs_closed": sum(1 for r in bugs if r["Status"].lower() in DONE),
        "completed": [brief(r) for r in done],
        "blocked": [brief(r) for r in open_ if r["Status"].lower() in BLOCKED],
        "carry_over": [brief(r) for r in open_],
    }, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
