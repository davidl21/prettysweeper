from fastapi import FastAPI
from models import Board
from typing import Optional

app = FastAPI()

game_board = Optional[Board] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}
