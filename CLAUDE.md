# CLAUDE.md

A small API with three layers: `src/app/api` (HTTP-facing), `src/app/*_service.py` (business rules),
`src/app/data` (storage). The code is a placeholder; the setup around it is the point.

## Commands

- Test: `python3 -m pytest -q`
- Sprint report numbers: `python3 .claude/skills/sprint-report/sprint_stats.py <export.csv>`

## Precedence

When rules conflict, the first match wins. A skill never outranks an earlier line.

1. The "never do" rules below.
2. CI must be green on every PR to `main`. Do not skip, delete or weaken a test to get there.
3. Skills in `.claude/skills/`, as playbooks.

## Never do

Each rule has a ratchet test in `tests/test_never_do_rules.py`. CI fails if a rule is broken,
whoever wrote the change. To change a rule, change this file and the test in the same PR,
and say why in the PR description. A human approves it.

- **R1: the API layer never imports the data layer.** Call a service. Test: `test_r1_…`.
- **R2: no customer data in source.** No real e-mail addresses or customer names in `src/`,
  not even to fix one customer's problem. Fix the code path instead. Test: `test_r2_…`.

## Working agreement

- Branch off `main`, open a PR, wait for green CI. You never merge your own PR.
- A failing test is evidence. Fix the code, not the assertion. If you think the test is wrong,
  stop and say so in the PR.
- Before reporting "done", run the tests and paste the result.
