from typing import List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="narde-engine")

class Player(BaseModel):
    id: int
    name: Optional[str] = None
    score: Optional[int] = 0

class StateResponse(BaseModel):
    state: str
    board: List  # keep generic for now; refine to a concrete type later
    turn: Optional[int] = None
    players: List[Player] = []
    current_player: Optional[int] = None

@app.get("/roll")
def roll(count: int = Query(2, ge=1, le=20), sides: int = Query(6, ge=2, le=100)):
    dice = [random.randint(1, sides) for _ in range(count)]
    logger.info("Rolled %d dice with %d sides: %s", count, sides, dice)
    return {"dice": dice}

@app.get("/state", response_model=StateResponse)
def get_state():
    # Minimal typed state expected by tests; replace with real game logic later.
    state = StateResponse(
        state="ok",
        board=[],
        turn=None,
        players=[],
        current_player=None
    )
    return state
