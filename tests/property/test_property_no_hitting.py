from hypothesis import given, strategies as st
from narde_engine.rules import validate_move_basic, normalize_piece

# simple board strategy: 8x8 with values in {0, "W", "B"}
cell = st.sampled_from([0, "W", "B"])
board_row = st.lists(cell, min_size=8, max_size=8)
board_strategy = st.lists(board_row, min_size=8, max_size=8)

coord = st.builds(lambda r, c: {"r": r, "c": c}, st.integers(0,7), st.integers(0,7))

@given(board=board_strategy, frm=coord, to=coord, turn=st.sampled_from(["W","B"]))
def test_no_hitting_property(board, frm, to, turn):
    # If destination contains opponent piece, validate_move_basic must reject
    dst_val = board[to["r"]][to["c"]]
    if normalize_piece(dst_val) is not None and normalize_piece(dst_val) != turn:
        valid, _ = validate_move_basic(turn, board, {"from": frm, "to": to})
        assert valid is False
