import yaml, os, textwrap
from pathlib import Path

spec = yaml.safe_load(open("rules/spec.yaml"))

# Templates keyed by rule id or check name (check takes precedence)
TEMPLATES = {
    "destination_must_not_be_opponent": """
def test_no_hitting():
    from narde_engine.rules import validate_move_basic
    board = [[0]*8 for _ in range(8)]
    board[5][0] = "B"
    board[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    valid, reason = validate_move_basic("W", board, move)
    assert valid is False
""",
    "single_step_forward": """
def test_single_step_forward_allowed():
    from narde_engine.rules import validate_move_basic
    board = [[0]*8 for _ in range(8)]
    board[6][0] = "W"
    ok  = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    bad = {"from": {"r": 6, "c": 0}, "to": {"r": 4, "c": 0}}
    assert validate_move_basic("W", board, ok)[0] is True
    assert validate_move_basic("W", board, bad)[0] is False
""",
    "max_consecutive": """
def test_max_consecutive_window():
    from narde_engine.rules import violates_consecutive_rule
    board = [[0]*8 for _ in range(8)]
    for c in range(2, 7):
        board[7][c] = "W"
    board[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 7, "c": 1}}
    assert violates_consecutive_rule("W", board, move, threshold=6) is True
""",
}

OUT_DIR = Path("tests/generated")
OUT_DIR.mkdir(parents=True, exist_ok=True)

generated = []
missing = []

for rule in spec.get("rules", []):
    rid = rule.get("id")
    # match on explicit check field first, then fall back to rule id
    key = rule.get("check") or rid
    if key in TEMPLATES:
        fname = OUT_DIR / f"test_rule_{rid}.py"
        body = textwrap.dedent(TEMPLATES[key]).strip()
        fname.write_text("import pytest\n\n" + body + "\n")
        generated.append(rid)
    else:
        missing.append(rid)

print("Generated tests for rules:", generated)
if missing:
    print("No template for rules:", missing)

# Run pytest on generated tests
print("\nRunning generated tests...")
ret = os.system(".venv/bin/pytest -q tests/generated")
if ret != 0:
    raise SystemExit(ret)

# Run full suite to ensure no regressions
print("\nRunning full test suite...")
ret = os.system(".venv/bin/pytest -q")
if ret != 0:
    raise SystemExit(ret)
