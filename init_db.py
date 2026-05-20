import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "narde_state.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            payload TEXT NOT NULL
        )
    """)
    cur.execute("SELECT COUNT(*) FROM game_state")
    if cur.fetchone()[0] == 0:
        initial = {
            "state": "ok",
            "board": {"width": 3, "height": 3, "cells": []},
            "turn": None,
            "players": [],
            "current_player": None
        }
        cur.execute("INSERT INTO game_state (id, payload) VALUES (1, ?)", (json.dumps(initial),))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Initialized DB at', DB_PATH)
