from typing import Dict, Any, List, Optional
from copy import deepcopy
from narde_engine.rules import validate_move_with_dice, simulate_move
from narde_engine.dice import consume_die

# Game state is expected to be a dict with keys:
# - board: List[List[Any]]
# - dice: List[int]
# - used: List[bool]
# - turn: "W" or "B"
# - history: List[Dict]  (optional; created if missing)
#
# Each history record:
# {
#   "board": <board snapshot before move>,
#   "used": <used snapshot before move>,
#   "consumed_die_indices": [..],
#   "move": <move object>,
#   "turn": <turn who moved>
# }

def apply_move_with_dice(turn: str, board: List[List[Any]], move: Dict[str, Dict[str,int]], dice: List[int], used: List[bool], game_state: Optional[Dict]=None) -> Dict[str, Any]:
    """
    Validate and apply a move using dice. If game_state provided, push a history record.
    Returns a response dict suitable for the UI.
    """
    if game_state is None:
        game_state = {}

    # Ensure history exists
    history = game_state.setdefault("history", [])

    valid, reason, die_idxs = validate_move_with_dice(turn, board, move, dice, used)
    if not valid:
        return {"valid": False, "reason": reason, "consumed_die_indices": [], "used": used, "board": board, "move": None}

    # Save snapshot before applying move
    snapshot = {
        "board": deepcopy(board),
        "used": list(used),
        "consumed_die_indices": list(die_idxs),
        "move": deepcopy(move),
        "turn": turn
    }
    history.append(snapshot)

    # consume the die indices returned (one or two)
    for idx in die_idxs:
        consume_die(used, idx)

    # apply the move to the board
    new_board = simulate_move(board, move)

    # update game_state board if provided
    game_state["board"] = new_board
    game_state["used"] = used
    game_state["dice"] = list(dice)
    game_state["turn"] = turn

    return {
        "valid": True,
        "reason": None,
        "consumed_die_indices": die_idxs,
        "used": used,
        "board": new_board,
        "move": move
    }

def undo_last_move(requesting_player: str, game_state: Dict[str, Any], allow_admin_override: bool=False) -> Dict[str, Any]:
    """
    Undo the last move in game_state history.
    - requesting_player: id or color of the player requesting undo (use your auth model)
    - allow_admin_override: if True, allow undo by admin even if not the mover
    Returns a response dict with restored state and which dice were re-enabled.
    """
    history = game_state.get("history", [])
    if not history:
        return {"valid": False, "reason": "no moves to undo", "restored_consumed_die_indices": [], "used": game_state.get("used"), "board": game_state.get("board"), "move_reverted": None}

    last = history[-1]
    mover = last.get("turn")

    # Permission check: only the mover can undo, unless admin override allowed
    if not allow_admin_override and requesting_player not in (mover, str(mover)):
        return {"valid": False, "reason": "permission denied to undo last move", "restored_consumed_die_indices": [], "used": game_state.get("used"), "board": game_state.get("board"), "move_reverted": None}

    # Pop and restore
    history.pop()
    restored_board = deepcopy(last["board"])
    restored_used = list(last["used"])
    restored_consumed = list(last.get("consumed_die_indices", []))
    move_reverted = deepcopy(last.get("move"))

    # Update game_state
    game_state["board"] = restored_board
    game_state["used"] = restored_used
    # dice values remain the same; only used flags change
    # Optionally update turn to the mover (so the same player can move again)
    game_state["turn"] = mover

    return {
        "valid": True,
        "reason": None,
        "restored_consumed_die_indices": restored_consumed,
        "used": restored_used,
        "board": restored_board,
        "move_reverted": move_reverted
    }
