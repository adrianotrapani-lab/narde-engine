from narde_engine.rules import validate_move_basic

def sample_board_empty():
    return [[0]*8 for _ in range(8)]

def test_single_step_forward_allowed():
    b = sample_board_empty()
    b[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    valid, reason = validate_move_basic("W", b, move)
    assert valid is True

def test_non_forward_non_capture_rejected():
    b = sample_board_empty()
    b[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 6, "c": 1}}
    valid, reason = validate_move_basic("W", b, move)
    assert valid is False
    assert "non-capturing" in reason.lower() or "illegal" in reason.lower()

def test_straight_into_opponent_rejected():
    b = sample_board_empty()
    b[6][0] = "W"
    b[5][0] = "B"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    valid, reason = validate_move_basic("W", b, move)
    assert valid is False
    assert "opponent" in reason.lower() or "no hitting" in reason.lower()

def test_stack_on_own_piece_allowed():
    b = sample_board_empty()
    b[6][0] = "W"
    b[5][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    valid, reason = validate_move_basic("W", b, move)
    assert valid is True
