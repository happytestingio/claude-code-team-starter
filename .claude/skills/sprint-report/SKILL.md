---
name: sprint-report
description: Turn a Jira sprint CSV export into the team's sprint report. Use when the user says "sprint report" and attaches or names a Jira CSV export.
---

# Sprint report

The numbers come from `sprint_stats.py`. You write the narrative. **Never compute,
round or re-count a number yourself.** If a number looks wrong, say so; do not fix it.

## Steps

1. Run `python3 sprint_stats.py <export.csv> --sprint "<sprint name>"` from this skill's folder
   (in this repo: `.claude/skills/sprint-report/`).
   If the user did not name the sprint, use the latest sprint in the file and say which one.
2. Read the JSON it prints. Fill `template.md` exactly: same headings, same order.
3. Write the narrative sections from the issue summaries in the JSON:
   - **Highlights:** at most 3 bullets, completed work that a customer would notice.
   - **Risks:** every blocked item, by key, with its summary. Do not invent causes.
   - **Carry-over:** list keys; one line on why only if a comment in the CSV says why.
4. Stop and ask when the CSV is missing a column the script needs. Do not guess.

## Team wording rules (the PM owns this list)

- Say "completed", not "done" or "closed".
- Story points as whole numbers.
- No names of individual developers in the report.
- [PM adds their own rules here during the session]
