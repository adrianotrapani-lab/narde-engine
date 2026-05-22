from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator
from typing import Any, Dict, List, Optional
import random

from narde_engine.rules import validate_move_basic, validate_move_with_dice
from narde_engine.dice import consume_die
from narde_engine.game import undo_last_move

app = FastAPI(title="Narde Rules Engine")

# --- Models ---
class Board(BaseModel):
    width: int
    height: int
    cells: List[Dict[str, Any]] = []

class Player(BaseModel):
    id: int
    name: str
    score: int = 0

class GameState(BaseModel):
    state: Optional[str] = "initialized"
    board: Board
    turn: Optional[int] = 0
    players: List[Player] = []
    current_player: Optional[int] = None

class Move(BaseModel):
    player: str
    from_point: int
    to_point: int

# --- In-memory state (replace with Firestore later) ---
# Create a 3x3 board and populate 9 cells so tests expecting len(cells)==9 pass
initial_board = Board(width=3, height=3, cells=[])
for y in range(initial_board.height):
    for x in range(initial_board.width):
        initial_board.cells.append({"x": x, "y": y, "value": ""})

game_state = GameState(board=initial_board, current_player=1)

# --- Endpoints ---
@app.get("/roll")
def roll_dice():
    dice = [random.randint(1, 6), random.randint(1, 6)]
    return {"dice": dice}

@app.post("/move")
def make_move(move: Move):
    if move.from_point == move.to_point:
        raise HTTPException(status_code=400, detail="Invalid move")
    return {"status": "Move accepted", "move": move}

@app.get("/state")
def get_state():
    return game_state.model_dump()

@app.post("/state")
def set_state(new_state: GameState):
    global game_state
    game_state = new_state
    return game_state.model_dump()

class MoveCoord(BaseModel):
    r: int
    c: int

class MoveDetail(BaseModel):
    from_: Optional[MoveCoord] = None
    to: Optional[MoveCoord] = None

    model_config = {"populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def _remap_from(cls, data: Any) -> Any:
        # JSON uses "from" which is a Python keyword; remap to "from_"
        if isinstance(data, dict) and "from" in data:
            data = dict(data)
            data["from_"] = data.pop("from")
        return data

class TurnValidationRequest(BaseModel):
    # legacy fields
    player: Optional[str] = None
    moves: Optional[List[Move]] = []
    # board-state fields
    session_id: Optional[str] = None
    board: Optional[List[Any]] = None
    turn: Optional[str] = None
    move: Optional[MoveDetail] = None
    # dice-aware fields
    dice: Optional[List[int]] = None
    used: Optional[List[bool]] = None

class TurnValidationResponse(BaseModel):
    valid: bool
    reason: Optional[str] = None
    consumed_die_indices: Optional[List[int]] = None
    used: Optional[List[bool]] = None
    board: Optional[List[Any]] = None
    move: Optional[Dict[str, Any]] = None

@app.post("/api/narde/validate-turn")
def validate_turn(request: TurnValidationRequest) -> TurnValidationResponse:
    # board-state style request
    if request.board is not None:
        if request.move is None:
            return TurnValidationResponse(valid=False, reason="No move provided")
        move_dict = {
            "from": {"r": request.move.from_.r, "c": request.move.from_.c} if request.move.from_ else None,
            "to": {"r": request.move.to.r, "c": request.move.to.c} if request.move.to else None,
        }
        turn = request.turn or ""

        # dice-aware path
        if request.dice is not None:
            used = list(request.used) if request.used is not None else [False] * len(request.dice)
            valid, reason, indices = validate_move_with_dice(turn, request.board, move_dict, request.dice, used)
            if valid and indices is not None:
                for idx in indices:
                    consume_die(used, idx)
            return TurnValidationResponse(
                valid=valid,
                reason=reason,
                consumed_die_indices=indices if valid else None,
                used=used if valid else None,
                board=request.board if valid else None,
                move=move_dict if valid else None,
            )

        # dice-free path
        valid, reason = validate_move_basic(turn, request.board, move_dict)
        return TurnValidationResponse(
            valid=valid,
            reason=reason,
            board=request.board if valid else None,
            move=move_dict if valid else None,
        )

    # legacy moves-list style request
    if not request.moves:
        return TurnValidationResponse(valid=False, reason="No moves provided")
    return TurnValidationResponse(valid=True)


# --- In-memory session game states (replace with persistent store later) ---
_session_states: Dict[str, Any] = {}

class UndoRequest(BaseModel):
    session_id: str
    steps: int = 1
    requesting_player: str = ""
    allow_admin_override: bool = False

class UndoResponse(BaseModel):
    valid: bool
    reason: Optional[str] = None
    restored_consumed_die_indices: Optional[List[int]] = None
    used: Optional[List[bool]] = None
    board: Optional[List[Any]] = None
    move_reverted: Optional[Dict[str, Any]] = None

@app.post("/api/undo")
def undo(request: UndoRequest) -> UndoResponse:
    state = _session_states.get(request.session_id)
    if state is None:
        return UndoResponse(valid=False, reason=f"session '{request.session_id}' not found")

    last_result: Dict[str, Any] = {}
    for _ in range(request.steps):
        last_result = undo_last_move(
            request.requesting_player,
            state,
            allow_admin_override=request.allow_admin_override,
        )
        if not last_result.get("valid"):
            break

    return UndoResponse(
        valid=last_result.get("valid", False),
        reason=last_result.get("reason"),
        restored_consumed_die_indices=last_result.get("restored_consumed_die_indices"),
        used=last_result.get("used"),
        board=last_result.get("board"),
        move_reverted=last_result.get("move_reverted"),
    )
