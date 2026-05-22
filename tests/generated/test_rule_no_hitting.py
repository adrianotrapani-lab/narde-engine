import pytest

def test_no_hitting():
    from narde_engine.rules import validate_move_basic
    board = [[0]*8 for _ in range(8)]
    board[5][0] = "B"
    board[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 5, "c": 0}}
    valid, reason = validate_move_basic("W", board, move)
    assert valid is False
