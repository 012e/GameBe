from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)

# Lazy imports (defer heavy imports)
def get_db():
    from app.database import get_db as _get_db
    return _get_db()

def get_trainer():
    from app.ai import bot_trainer
    return bot_trainer

def get_game_model():
    from app.models.game import GameCreate
    return GameCreate

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/games/", methods=["POST"])
def save_game():
    data = request.get_json(silent=True)
    if not data:
        raise BadRequest("Missing JSON body")

    db = get_db()
    GameCreate = get_game_model()
    game = GameCreate(**data)

    db.insert_one(game.dict())
    games = list(db.find())

    get_trainer().train_mcts(games)

    return jsonify({"message": "Game saved and bot trained"})

@app.route("/bot-move/", methods=["POST"])
def get_bot_move():
    data = request.get_json(silent=True)
    if not data:
        raise BadRequest("Missing JSON body")

    board = data.get("board")
    current_player = data.get("current_player")

    if board is None or current_player is None:
        raise BadRequest("Board and current_player are required")

    move = get_trainer().get_trained_move(board, current_player)
    if not move:
        raise NotFound("No valid move found")

    return jsonify(move)

