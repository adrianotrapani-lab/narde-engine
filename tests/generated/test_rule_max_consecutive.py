import pytest

def test_max_consecutive_window():
    from narde_engine.rules import violates_consecutive_rule
    board = [[0]*8 for _ in range(8)]
    for c in range(2, 7):
        board[7][c] = "W"
    board[6][0] = "W"
    move = {"from": {"r": 6, "c": 0}, "to": {"r": 7, "c": 1}}
    assert violates_consecutive_rule("W", board, move, threshold=6) is True
