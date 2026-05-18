from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="Narde Rules Engine")

# --- Models ---
class Move(BaseModel):
    player: str
    from_point: int
    to_point: int

class GameState(BaseModel):
    board: dict
    current_player: str

# --- In-memory state (replace with Firestore later) ---
game_state = GameState(board={}, current_player="Player1")

# --- Endpoints ---
@app.get("/roll")
def roll_dice():
    dice = [random.randint(1, 6), random.randint(1, 6)]
    return {"dice": dice}

@app.post("/move")
def make_move(move: Move):
    # Placeholder validation
    if move.from_point == move.to_point:
        raise HTTPException(status_code=400, detail="Invalid move")
    return {"status": "Move accepted", "move": move}

@app.get("/state")
def get_state():
    return game_state
