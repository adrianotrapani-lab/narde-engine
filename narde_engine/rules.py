from typing import Any, Dict, List, Optional, Tuple

from narde_engine.dice import choose_die_index

Board = List[List[Any]]
Coord = Dict[str, int]

def coord_value(board: Board, coord: Coord) -> Optional[Any]:
    try:
        r, c = coord["r"], coord["c"]
        return board[r][c]
    except Exception:
        return None

def normalize_piece(piece: Any) -> Optional[str]:
    if piece is None:
        return None
    if piece == 0:
        return None
    try:
        s = str(piece).strip().upper()
        if s in ("W", "B"):
            return s
    except Exception:
        pass
    return None

def is_own_piece(turn: str, piece: Any) -> bool:
    p = normalize_piece(piece)
    if p is None:
        return False
    return p == str(turn).upper()

def is_opponent_piece(turn: str, piece: Any) -> bool:
    p = normalize_piece(piece)
    if p is None:
        return False
    return p != str(turn).upper()

def is_single_step_forward(from_coord: Coord, to_coord: Coord, turn: str) -> bool:
    try:
        fr, fc = from_coord["r"], from_coord["c"]
        tr, tc = to_coord["r"], to_coord["c"]
    except Exception:
        return False
    if fc != tc:
        return False
    if str(turn).upper() == "W":
        return tr == fr - 1
    return tr == fr + 1

def simulate_move(board: Board, move: Dict[str, Coord]) -> Board:
    sim = [list(row) for row in board]
    try:
        fr, fc = move["from"]["r"], move["from"]["c"]
        tr, tc = move["to"]["r"], move["to"]["c"]
    except Exception:
        return sim
    try:
        piece = sim[fr][fc]
    except Exception:
        piece = None
    try:
        sim[tr][tc] = piece
    except Exception:
        pass
    try:
        sim[fr][fc] = 0
    except Exception:
        pass
    return sim

def normalize_player(player: str) -> str:
    return str(player).upper()

def violates_consecutive_rule(turn: str, board: Board, move: Dict[str, Coord], threshold: int = 6) -> bool:
    sim = simulate_move(board, move)
    player = normalize_player(turn)
    opponent = "B" if player == "W" else "W"

    rows = len(sim)
    cols = len(sim[0]) if rows else 0

    # scan rows
    for r in range(rows):
        row = sim[r]
        for start in range(0, cols - threshold + 1):
            window = row[start:start + threshold]
            mover_count = sum(1 for v in window if normalize_piece(v) == player)
            opp_count = sum(1 for v in window if normalize_piece(v) == opponent)
            if mover_count >= threshold and opp_count == 0:
                return True

    # scan columns
    for c in range(cols):
        col = [sim[r][c] for r in range(rows)]
        for start in range(0, rows - threshold + 1):
            window = col[start:start + threshold]
            mover_count = sum(1 for v in window if normalize_piece(v) == player)
            opp_count = sum(1 for v in window if normalize_piece(v) == opponent)
            if mover_count >= threshold and opp_count == 0:
                return True

    return False

def validate_move_basic(turn: str, board: Board, move: Dict[str, Coord]) -> Tuple[bool, Optional[str]]:
    if not isinstance(move, dict) or "from" not in move or "to" not in move:
        return False, "invalid move shape"

    from_coord = move.get("from")
    to_coord = move.get("to")

    src = coord_value(board, from_coord)
    dst = coord_value(board, to_coord)

    if src is None or src == 0:
        return False, "no piece at source"

    if not is_own_piece(turn, src):
        return False, "piece does not belong to current player"

    # If destination contains opponent piece -> invalid in Narde (no hitting)
    if dst is not None and dst != 0 and is_opponent_piece(turn, dst):
        return False, "destination occupied by opponent (Narde: no hitting allowed)"

    # If destination contains same-color piece -> allowed (stacking)
    if dst is not None and dst != 0 and is_own_piece(turn, dst):
        if violates_consecutive_rule(turn, board, move, threshold=6):
            return False, "would create forbidden run of 6+ consecutive checkers with no opponent present"
        return True, None

    # destination empty: allow only single-step forward
    if dst is None or dst == 0:
        if is_single_step_forward(from_coord, to_coord, turn):
            if violates_consecutive_rule(turn, board, move, threshold=6):
                return False, "would create forbidden run of 6+ consecutive checkers with no opponent present"
            return True, None
        return False, "illegal non-capturing move"

    return False, "unhandled move case"


def enumerate_single_step_forward_moves(turn: str, board: Board) -> List[Dict[str, Coord]]:
    """
    Return all legal single-step forward moves for `turn` on the given board.
    Uses validate_move_basic to check legality (so it respects stacking and consecutive rule).
    """
    moves = []
    rows = len(board)
    cols = len(board[0]) if rows else 0
    for r in range(rows):
        for c in range(cols):
            if normalize_piece(board[r][c]) == str(turn).upper():
                from_coord = {"r": r, "c": c}
                # forward target
                if str(turn).upper() == "W":
                    to_r = r - 1
                else:
                    to_r = r + 1
                to_c = c
                if 0 <= to_r < rows:
                    move = {"from": from_coord, "to": {"r": to_r, "c": to_c}}
                    valid, _ = validate_move_basic(turn, board, move)
                    if valid:
                        moves.append(move)
    return moves


def select_move_max_followups(turn: str, board: Board, candidate_moves: List[Dict[str, Coord]], followup_steps: int = 1) -> Optional[Dict[str, Coord]]:
    """
    Given a list of candidate first moves, simulate each and count how many legal follow-up
    single-step-forward moves exist for `followup_steps` iterations (simple greedy depth=followup_steps).
    Returns the candidate move that yields the largest count (ties broken by first candidate).
    """
    if not candidate_moves:
        return None

    best_move = None
    best_score = -1

    for mv in candidate_moves:
        sim = simulate_move(board, mv)
        # simple greedy: count available single-step moves after applying mv
        score = 0
        # for followup_steps > 1 we repeat simulation greedily (not exhaustive)
        current_board = sim
        for _ in range(followup_steps):
            next_moves = enumerate_single_step_forward_moves(turn, current_board)
            score += len(next_moves)
            # if there is at least one move, simulate the first to continue counting
            if next_moves:
                current_board = simulate_move(current_board, next_moves[0])
            else:
                break

        if score > best_score:
            best_score = score
            best_move = mv

    return best_move


def path_clear_for_combined_move(turn: str, board: Board, from_coord: Coord, distance: int) -> bool:
    """Return True if every intermediate step up to distance is not occupied by opponent
    and destination is not occupied by opponent (Narde: no hitting)."""
    try:
        fr, fc = from_coord["r"], from_coord["c"]
    except Exception:
        return False
    rows = len(board)
    # direction: white moves up (r-1), black moves down (r+1)
    step = -1 if str(turn).upper() == "W" else 1
    for step_i in range(1, distance + 1):
        tr = fr + step_i * step
        tc = fc
        if not (0 <= tr < rows):
            return False
        val = board[tr][tc]
        if is_opponent_piece(turn, val):
            return False
    return True


def validate_combined_move(turn: str, board: Board, move: Dict[str, Coord], dice: List[int], used: List[bool]) -> Tuple[bool, Optional[List[int]]]:
    """If move distance equals sum of two unused dice and path is clear and consecutive rule ok,
    return (True, [i,j]) indices of dice to consume. Otherwise (False, reason)."""
    # compute distance
    try:
        fr, fc = move["from"]["r"], move["from"]["c"]
        tr, tc = move["to"]["r"], move["to"]["c"]
    except Exception:
        return False, "invalid coords"
    distance = abs(tr - fr)  # columns unchanged in our model
    # find indices of unused dice
    unused = [i for i, u in enumerate(used) if not u]
    if len(unused) < 2:
        return False, "not enough unused dice for combined move"
    # check if any pair of unused dice sums to distance
    pairs = []
    for i in range(len(unused)):
        for j in range(i + 1, len(unused)):
            a, b = unused[i], unused[j]
            if dice[a] + dice[b] == distance:
                pairs.append((a, b))
    if not pairs:
        return False, "no dice pair sums to move distance"
    # for determinism pick the pair with deterministic tie-break (lowest indices)
    a, b = pairs[0]
    # path clearance and destination no-hitting
    if not path_clear_for_combined_move(turn, board, move["from"], distance):
        return False, "path blocked by opponent"
    # simulate and check consecutive rule
    if violates_consecutive_rule(turn, board, move, threshold=6):
        return False, "would create forbidden run of 6+ consecutive checkers"
    # destination must not be opponent (already checked by path_clear but double-check)
    dst = coord_value(board, move["to"])
    if dst is not None and dst != 0 and is_opponent_piece(turn, dst):
        return False, "destination occupied by opponent"
    return True, [a, b]


def validate_move_with_dice(turn: str, board: Board, move: Dict[str, Coord], dice: List[int], used: List[bool]) -> Tuple[bool, Optional[str], Optional[List[int]]]:
    """
    Dice-aware validator.
    Returns (valid, reason_or_None, die_indices_to_consume_or_None).
    """
    # try combined move first
    ok, info = validate_combined_move(turn, board, move, dice, used)
    if ok:
        return True, None, info  # info is list of two indices
    # fallback: single-die move using existing validate_move_basic
    valid, reason = validate_move_basic(turn, board, move)
    if not valid:
        return False, reason, None
    # choose die index for the single-die distance
    try:
        fr = move["from"]["r"]
        tr = move["to"]["r"]
        distance = abs(tr - fr)
    except Exception:
        return False, "invalid coords", None
    idx = choose_die_index(dice, used, distance, move["from"])
    if idx is None:
        return False, "no available die for move", None
    return True, None, [idx]
