from narde_engine.rules import violates_consecutive_rule, validate_move_basic


def test_no_violation_normal_move():
    """A standard forward step on a sparse board should not trigger the rule."""
    b = [[0]*8 for _ in range(8)]
    b[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    assert violates_consecutive_rule("W", b, move, threshold=6) is False


def test_violation_row_of_six():
    """Moving W into a row that completes 6 consecutive W pieces (no B) triggers the rule."""
    b = [[0]*8 for _ in range(8)]
    # Row 5: W at cols 1-5 (5 pieces); moving W from (6,0) to (5,0) makes cols 0-5 all W
    b[5] = [0,"W","W","W","W","W",0,0]
    b[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    assert violates_consecutive_rule("W", b, move, threshold=6) is True


def test_violation_blocked_by_opponent():
    """A B piece inside the window prevents a violation."""
    b = [[0]*8 for _ in range(8)]
    # Row 5: W at cols 1-2, B at col 3, W at cols 4-5 — no 6-window is all-W
    b[5] = [0,"W","W","B","W","W",0,0]
    b[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    assert violates_consecutive_rule("W", b, move, threshold=6) is False


def test_validate_move_basic_rejects_consecutive_violation():
    """validate_move_basic rejects a single-step forward move that creates a forbidden 6-run."""
    b = [[0]*8 for _ in range(8)]
    b[5] = [0,"W","W","W","W","W",0,0]
    b[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    valid, reason = validate_move_basic("W", b, move)
    assert valid is False
    assert "consecutive" in reason.lower() or "forbidden" in reason.lower() or "run" in reason.lower()


def test_stacking_triggers_consecutive_violation():
    """Stacking onto own piece is allowed unless it creates a 6-run."""
    b = [[0]*8 for _ in range(8)]
    # Row 5: W at cols 0-4 (5 pieces); stacking W from (6,5) onto (5,5) makes cols 0-5 all W
    b[5] = ["W","W","W","W","W",0,0,0]
    b[6][5] = "W"
    b[5][5] = "W"  # destination already has W (stacking scenario)
    move = {"from": {"r": 6, "c": 5}, "to": {"r": 5, "c": 5}}
    valid, reason = validate_move_basic("W", b, move)
    assert valid is False
    assert "consecutive" in reason.lower() or "forbidden" in reason.lower() or "run" in reason.lower()
