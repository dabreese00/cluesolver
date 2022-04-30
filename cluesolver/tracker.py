from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request
from cluesolver.db import get_db


bp = Blueprint('tracker', __name__)


@bp.route('/games', methods=['GET', 'POST'])
def games():
    db = get_db()
    response = None

    if request.method == 'POST':
        game_json = request.get_json()
        try:
            name = game_json['name']
        except KeyError:
            response = ({'error': 'Game name is required.'}, 401)

        if response is None:
            try:
                db.execute(
                    "INSERT INTO game (name) VALUES (:name)", {'name': name}
                )
                db.commit()
            except IntegrityError:
                response = ({'error': f"Game {name} already exists."}, 401)
            else:
                response = ({'name': name}, 201)

    elif request.method == 'GET':
        games = [dict(g) for g in db.execute("SELECT * FROM game").fetchall()]
        response = ({'games': games}, 200)

    return response


@bp.route('/games/<name>')
def game_detail(name):
    db = get_db()

    game = db.execute(
        "SELECT * FROM game WHERE game.name = :name",
        {'name': name}
    ).fetchone()

    if game is not None:
        response = ({'name': name}, 200)
    else:
        response = ({}, 404)

    return response
