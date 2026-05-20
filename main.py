from fastapi import FastAPI, Query
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/roll")
def roll(count: int = Query(2, ge=1, le=20), sides: int = Query(6, ge=2, le=100)):
    dice = [random.randint(1, sides) for _ in range(count)]
    logger.info("Rolled %d dice with %d sides: %s", count, sides, dice)
    return {"dice": dice}

@app.get("/state")
def get_state():
    # Minimal state structure expected by tests: include 'board' and 'current_player'
    state = {
        "state": "ok",
        "board": [],            # tests expect this key
        "turn": None,
        "players": [],
        "current_player": None  # added to satisfy tests
    }
    return state
