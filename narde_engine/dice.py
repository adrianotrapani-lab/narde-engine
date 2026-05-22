from typing import List, Optional, Dict

def choose_die_index(dice: List[int], used: List[bool], move_distance: int, from_coord: Dict[str,int]) -> Optional[int]:
    """
    Choose which die index to consume for a move of `move_distance`.
    - dice: list of die face values, length 2 (e.g., [2,3] or [4,4] for doubles)
    - used: parallel list of booleans indicating whether each die is already consumed
    - move_distance: integer number of points moved
    - from_coord: source coordinate dict used to break ties deterministically
    Returns index 0 or 1, or None if no unused die is available.
    Tie-break rule when both unused dice match move_distance:
      use parity of source coordinate (r + c) % 2 to pick index 0 or 1.
    """
    # Validate inputs
    if not dice or not used or len(dice) != len(used):
        return None

    # Collect indices of unused dice
    unused_idxs = [i for i, u in enumerate(used) if not u]
    if not unused_idxs:
        return None

    # First, prefer unused dice that exactly match move_distance
    exact_matches = [i for i in unused_idxs if dice[i] == move_distance]
    if len(exact_matches) == 1:
        return exact_matches[0]
    if len(exact_matches) >= 2:
        # tie-break deterministically by source coordinate parity
        try:
            parity = (int(from_coord.get("r", 0)) + int(from_coord.get("c", 0))) & 1
        except Exception:
            parity = 0
        # Map parity 0 -> choose first exact match by index order, parity 1 -> choose second if exists
        # Ensure we return a valid index from exact_matches
        if parity == 0:
            return exact_matches[0]
        else:
            # if only two dice, prefer the other one; otherwise fallback to first
            return exact_matches[1] if len(exact_matches) > 1 else exact_matches[0]

    # No exact match: prefer smallest unused die >= move_distance
    ge_candidates = [i for i in unused_idxs if dice[i] >= move_distance]
    if ge_candidates:
        # choose the smallest die value among candidates; tie-break by index
        best = min(ge_candidates, key=lambda i: (dice[i], i))
        return best

    # Fallback: choose the largest unused die (greedy fallback)
    fallback = max(unused_idxs, key=lambda i: (dice[i], -i))
    return fallback

def consume_die(used: List[bool], idx: int) -> None:
    """Mark die at idx as used. Mutates used list in place."""
    if idx is None:
        return
    if 0 <= idx < len(used):
        used[idx] = True
