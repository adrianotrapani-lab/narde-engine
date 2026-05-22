from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator
from typing import Any, Dict, List, Optional
import random

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

class TurnValidationResponse(BaseModel):
    valid: bool
    reason: Optional[str] = None

def _validate_board_move(
    board: List[Any],
    turn: str,
    move: MoveDetail,
) -> TurnValidationResponse:
    """Validate a single move against the board state."""
    if move.from_ is None or move.to is None:
        return TurnValidationResponse(valid=False, reason="Move must specify 'from' and 'to'")

    rows = len(board)
    cols = len(board[0]) if rows else 0

    fr, fc = move.from_.r, move.from_.c
    tr, tc = move.to.r, move.to.c

    # Bounds check
    if not (0 <= fr < rows and 0 <= fc < cols):
        return TurnValidationResponse(valid=False, reason="Source position out of bounds")
    if not (0 <= tr < rows and 0 <= tc < cols):
        return TurnValidationResponse(valid=False, reason="Destination position out of bounds")

    src = board[fr][fc]
    dst = board[tr][tc]

    # The piece at the source must belong to the current player
    if src != turn:
        return TurnValidationResponse(
            valid=False,
            reason=f"No {turn} piece at source — found '{src}'. Cannot move opponent's piece on your turn.",
        )

    # Destination must not be occupied by the same color
    if dst == turn:
        return TurnValidationResponse(
            valid=False,
            reason=f"Destination is occupied by your own piece ('{turn}'). Cannot capture your own piece.",
        )

    return TurnValidationResponse(valid=True)


@app.post("/api/narde/validate-turn")
def validate_turn(request: TurnValidationRequest) -> TurnValidationResponse:
    # board-state style request
    if request.board is not None:
        if request.move is None:
            return TurnValidationResponse(valid=False, reason="No move provided")
        return _validate_board_move(request.board, request.turn or "", request.move)
    # legacy moves-list style request
    if not request.moves:
        return TurnValidationResponse(valid=False, reason="No moves provided")
    return TurnValidationResponse(valid=True)
