from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from app.ai.bot_trainer import get_trained_move, train_mcts
from app.database import get_db
from app.models.game import GameCreate

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/games/", methods=["POST"])
def save_game():
    db = get_db()
    data = request.get_json()
    if not data:
        raise BadRequest("Missing JSON body")

    game = GameCreate(**data)
    db.insert_one(game.dict())
    games = list(db.find())
    train_mcts(games)
    return jsonify({"message": "Game saved and bot trained"})


@app.route("/bot-move/", methods=["POST"])
def get_bot_move():
    data = request.get_json()
    if not data:
        raise BadRequest("Missing JSON body")

    board = data.get("board")
    current_player = data.get("current_player")

    if not board or not current_player:
        raise BadRequest("Board and current_player are required")

    move = get_trained_move(board, current_player)
    if not move:
        raise NotFound("No valid move found")

    return jsonify(move)
