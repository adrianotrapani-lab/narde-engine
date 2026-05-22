# narde_engine/game.py
from typing import Dict, Any, List
from narde_engine.rules import validate_move_with_dice, simulate_move
from narde_engine.dice import consume_die

def apply_move_with_dice(turn: str, board: List[List[Any]], move: Dict[str, Dict[str,int]], dice: List[int], used: List[bool]) -> Dict[str, Any]:
    """
    Validate and apply a move using dice. Returns a response dict suitable for the UI.
    - turn: "W" or "B"
    - board: current board
    - move: {"from": {"r":..,"c":..}, "to": {...}}
    - dice: [d1, d2]
    - used: [bool, bool]
    """
    valid, reason, die_idxs = validate_move_with_dice(turn, board, move, dice, used)
    if not valid:
        return {"valid": False, "reason": reason, "consumed_die_indices": [], "used": used, "board": board, "move": None}

    # consume the die indices returned (one or two)
    for idx in die_idxs:
        consume_die(used, idx)

    # apply the move to the board
    new_board = simulate_move(board, move)

    return {
        "valid": True,
        "reason": None,
        "consumed_die_indices": die_idxs,
        "used": used,
        "board": new_board,
        "move": move
    }
