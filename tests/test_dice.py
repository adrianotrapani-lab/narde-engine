from narde_engine.dice import choose_die_index, consume_die

def test_choose_exact_single_match():
    dice = [2, 3]
    used = [False, False]
    idx = choose_die_index(dice, used, 2, {"r":6,"c":0})
    assert idx == 0
    consume_die(used, idx)
    assert used == [True, False]

def test_choose_exact_both_match_uses_parity():
    dice = [2, 2]
    used = [False, False]
    # parity 0 -> choose index 0
    idx0 = choose_die_index(dice, used, 2, {"r":6,"c":0})
    assert idx0 == 0
    # parity 1 -> choose index 1
    used = [False, False]
    idx1 = choose_die_index(dice, used, 2, {"r":6,"c":1})
    assert idx1 == 1

def test_choose_no_exact_prefers_ge():
    dice = [2, 5]
    used = [False, False]
    # move_distance 3 -> prefer die 5 (>=3) over die 2
    idx = choose_die_index(dice, used, 3, {"r":0,"c":0})
    assert idx == 1

def test_choose_fallback_when_all_smaller():
    dice = [1, 1]
    used = [False, False]
    idx = choose_die_index(dice, used, 3, {"r":0,"c":0})
    # fallback chooses the largest unused die (both equal) -> index 0 by tie-break
    assert idx in (0,1)
    consume_die(used, idx)
    # second call should return the other die
    idx2 = choose_die_index(dice, used, 3, {"r":0,"c":0})
    assert idx2 is not None
