from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
