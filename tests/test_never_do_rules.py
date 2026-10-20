"""Ratchets for the "never do" rules in CLAUDE.md.

Claude Code reads the rule; this test enforces it in CI. Either one alone drifts.
"""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
            mods.update(f"{node.module}.{a.name}" for a in node.names)
    return mods


def test_r1_api_layer_never_imports_the_data_layer():
    offenders = [
        str(f.relative_to(ROOT))
        for f in (SRC / "app" / "api").rglob("*.py")
        if any(m.startswith("src.app.data") for m in imported_modules(f))
    ]
    assert offenders == [], "R1: call the service layer instead"


# R2: no customer data in source. Add real customer names here when one leaks once.
BANNED_IN_SRC = [re.compile(r"[\w.+-]+@(?!example\.)[\w-]+\.[\w.]+")]


def test_r2_no_customer_data_in_source():
    hits = [
        str(f.relative_to(ROOT))
        for f in SRC.rglob("*.py")
        for pattern in BANNED_IN_SRC
        if pattern.search(f.read_text(encoding="utf-8"))
    ]
    assert hits == []
