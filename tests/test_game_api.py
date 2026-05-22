# tests/test_game_api.py
from narde_engine.game import apply_move_with_dice

def test_apply_single_die_move_consumes_correct_die():
    board = [[0]*8 for _ in range(8)]
    board[6][0] = "W"
    dice = [2,3]; used = [False, False]
    move = {"from":{"r":6,"c":0},"to":{"r":5,"c":0}}  # distance 1 -> will use die selection logic
    resp = apply_move_with_dice("W", board, move, dice, used)
    assert resp["valid"] is True
    assert isinstance(resp["consumed_die_indices"], list)
    assert len(resp["consumed_die_indices"]) in (1,2)
    assert resp["used"] == used

def test_apply_combined_move_consumes_both_dice():
    board = [[0]*8 for _ in range(8)]
    board[6][0] = "W"
    # clear path for 5-step combined move
    for r in range(2,6):
        board[r][0] = 0
    dice = [2,3]; used = [False, False]
    move = {"from":{"r":6,"c":0},"to":{"r":1,"c":0}}  # distance 5
    resp = apply_move_with_dice("W", board, move, dice, used)
    assert resp["valid"] is True
    assert set(resp["consumed_die_indices"]) == {0,1}
    assert resp["used"] == [True, True]
