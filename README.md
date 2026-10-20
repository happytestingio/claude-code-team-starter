# Claude Code team starter

A small, working example of the Claude Code setup I bring to a team in week 1: the repo
files that make an AI coding agent safe to adopt, plus one skill a non-developer can run.

The application code is a placeholder. The setup around it is the point.

| File | What it shows |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Commands, a precedence order (a skill never outranks a rule), "never do" rules with ids, and the working agreement: the agent never merges its own PR |
| [`.claude/settings.json`](.claude/settings.json) | Committed permissions. **Allow:** tests, read-only git and gh. **Ask:** push, PR create/merge, installs, edits to CI and to the ratchet test. **Deny:** force-push, hard reset, `rm -rf`, admin merge, reading `.env` |
| [`tests/test_never_do_rules.py`](tests/test_never_do_rules.py) | Ratchet tests: each CLAUDE.md rule fails CI when broken, whoever wrote the change |
| [`.claude/skills/sprint-report/`](.claude/skills/sprint-report/) | A skill that turns a Jira CSV export into the team's sprint report. A script does the arithmetic; the model only writes the narrative |
| [`tests/test_sprint_report_golden.py`](tests/test_sprint_report_golden.py) | Golden test: the report numbers can't drift, and a missing CSV column fails loudly instead of being guessed |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | The one required check. With branch protection on `main`, nothing merges red |
| [`docs/never-do-rule-pattern.md`](docs/never-do-rule-pattern.md) | Why the rule + test + guard pattern works, and the same pattern in xUnit for .NET teams |

## Run it

```bash
python3 -m pip install pytest
python3 -m pytest -q
python3 .claude/skills/sprint-report/sprint_stats.py .claude/skills/sprint-report/fixtures/sample-export.csv
```

Then open the repo in Claude Code and type `sprint report` with the sample CSV.

## The sprint-report skill, in one session

The skill is built *with* the person who writes the report today, on their machine, in about 90 minutes:

1. Watch the current process and keep its output as the golden report.
2. Their written instructions become `SKILL.md`, the layout becomes `template.md`, and
   `sprint_stats.py` computes the numbers deterministically.
3. Run it on the last two sprints and compare with the reports actually sent, until they would send it unchanged.
4. They run it alone from a fresh chat. It's versioned here, maintained like code.

A later step replaces the CSV with a Jira MCP connection.

---

Paul de Witt · [happytesting.io](https://happytesting.io)
See also: [orchestration-playwright-agents](https://github.com/happytestingio/orchestration-playwright-agents) · [orchestration-cypress-agents](https://github.com/happytestingio/orchestration-cypress-agents)
