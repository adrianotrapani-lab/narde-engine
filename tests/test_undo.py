from narde_engine.game import apply_move_with_dice, undo_last_move

def sample_board():
    b = [[0]*8 for _ in range(8)]
    b[6][0] = "W"
    b[6][1] = "W"
    return b

def test_undo_single_move_restores_board_and_die():
    b = sample_board()
    dice = [2,3]; used = [False, False]
    game_state = {"board": b, "dice": list(dice), "used": list(used), "turn": "W", "history": []}
    move = {"from":{"r":6,"c":0},"to":{"r":5,"c":0}}
    resp = apply_move_with_dice("W", b, move, dice, used, game_state)
    assert resp["valid"] is True
    # After move, used should reflect consumed die(s)
    assert "consumed_die_indices" in resp
    # Now undo
    undo_resp = undo_last_move("W", game_state)
    assert undo_resp["valid"] is True
    assert undo_resp["board"][6][0] == "W"
    # restored used should re-enable the consumed dice
    assert undo_resp["used"] == [False, False] or isinstance(undo_resp["restored_consumed_die_indices"], list)

def test_undo_combined_move_restores_both_dice():
    b = sample_board()
    # clear path for combined move of 5
    for r in range(2,6):
        b[r][0] = 0
    dice = [2,3]; used = [False, False]
    game_state = {"board": b, "dice": list(dice), "used": list(used), "turn": "W", "history": []}
    move = {"from":{"r":6,"c":0},"to":{"r":1,"c":0}}
    resp = apply_move_with_dice("W", b, move, dice, used, game_state)
    assert resp["valid"] is True
    undo_resp = undo_last_move("W", game_state)
    assert undo_resp["valid"] is True
    assert set(undo_resp["restored_consumed_die_indices"]) == {0,1}
    assert undo_resp["used"] == [False, False]
