import pytest

def test_single_step_forward_allowed():
    from narde_engine.rules import validate_move_basic
    board = [[0]*8 for _ in range(8)]
    board[6][0] = "W"
    ok = {'from':{'r':6,'c':0}, 'to':{'r':5,'c':0}}
    bad = {'from':{'r':6,'c':0}, 'to':{'r':4,'c':0}}
    assert validate_move_basic("W", board, ok)[0] is True
    assert validate_move_basic("W", board, bad)[0] is False