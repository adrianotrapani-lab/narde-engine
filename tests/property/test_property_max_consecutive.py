from hypothesis import given, strategies as st
from narde_engine.rules import violates_consecutive_rule, normalize_piece

cell = st.sampled_from([0, "W", "B"])
board_row = st.lists(cell, min_size=8, max_size=8)
board_strategy = st.lists(board_row, min_size=8, max_size=8)

coord = st.builds(lambda r, c: {"r": r, "c": c}, st.integers(0,7), st.integers(0,7))

@given(board=board_strategy, frm=coord, to=coord, turn=st.sampled_from(["W","B"]))
def test_max_consecutive_property(board, frm, to, turn):
    # If a window of length 6 after the move would contain only mover pieces, the rule should detect it.
    # We only assert that the function runs and returns a boolean; concrete failures are caught by deterministic tests.
    res = violates_consecutive_rule(turn, board, {"from": frm, "to": to}, threshold=6)
    assert isinstance(res, bool)
