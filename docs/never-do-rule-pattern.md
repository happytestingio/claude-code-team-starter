# Pattern: a "never do" rule that a test enforces

Claude Code reads the rule. CI enforces it. Either one alone drifts: a rule with no test gets
argued away in a long session, and a test with no rule gets "fixed" by loosening the assertion.

The pattern comes from a production SaaS where Claude Code writes most PRs. Its strongest rule
is *fix the generator, never patch one customer's live output*. A ratchet test fails the build if
a retired per-customer patch module comes back, or if a customer's name appears in `src/`.

## Three parts, always together

1. **The rule, in CLAUDE.md**, with an id and the name of its test. See `CLAUDE.md` → "Never do".
2. **The ratchet test**, in the required CI job. See `tests/test_never_do_rules.py`.
3. **A guard on the guard.** `.claude/settings.json` puts edits to the ratchet test and to the
   workflows under `ask`, so Claude Code can't quietly weaken them. Branch protection requires CI.

## Try it

```bash
echo "from src.app.data import orders_repo" >> src/app/api/orders.py
python3 -m pytest -q   # fails: R1: call the service layer instead
git checkout src/app/api/orders.py
```

## The same pattern in .NET / Azure DevOps

```csharp
// tests/Architecture/NeverDoRules.cs  (xUnit)
public class NeverDoRules
{
    [Fact]
    public void R1_controllers_do_not_reference_the_data_layer()
    {
        var offenders = Directory
            .EnumerateFiles(RepoRoot("src/Api/Controllers"), "*.cs", SearchOption.AllDirectories)
            .Where(f => File.ReadAllText(f).Contains("using App.Data."))
            .ToList();
        Assert.Empty(offenders);
    }
}
```

In Azure DevOps the "required CI" part is a branch policy with build validation on `main`.
