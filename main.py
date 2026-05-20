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

class Cell(BaseModel):
    x: int
    y: int
    value: Optional[str] = None

class Board(BaseModel):
    width: int
    height: int
    cells: List[Cell] = []

class StateResponse(BaseModel):
    state: str
    board: Board
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
    # Example board: 3x3 empty cells
    cells = [Cell(x=x, y=y, value=None) for y in range(3) for x in range(3)]
    board = Board(width=3, height=3, cells=cells)
    state = StateResponse(
        state="ok",
        board=board,
        turn=None,
        players=[],
        current_player=None
    )
    return state
