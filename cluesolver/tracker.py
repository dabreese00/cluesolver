from sqlalchemy.exc import NoResultFound
from flask import Blueprint, request

from cluesolver.db import get_db, get_repo
from cluesolver.cluegame import Game, Player


bp = Blueprint('tracker', __name__)


def serialize_game(game):
    return {'name': game.name}


def deserialize_game(json):
    return Game(json['name'])


@bp.route('/games', methods=['GET', 'POST'])
def games():
    db = get_db()
    repo = get_repo()
    response = None

    if request.method == 'POST':
        try:
            game = deserialize_game(request.get_json())
        except KeyError:
            response = ({'error': 'Missing parameter.'}, 401)
        else:
            repo.add(game)
            db.commit()
            response = (serialize_game(game), 201)

    elif request.method == 'GET':
        games = [serialize_game(g) for g in repo.list()]
        response = ({'games': games}, 200)

    return response


@bp.route('/games/<name>')
def game_detail(name):
    repo = get_repo()

    try:
        game = repo.get(name)
    except NoResultFound as e:
        response = ({'error': str(e)}, 404)
    else:
        response = (serialize_game(game), 200)

    return response


def serialize_player(player):
    return {
        'name': player.name,
        'hand_size': player.hand_size,
        'game_name': player.game.name,
    }


def deserialize_player(json):
    return Player(json['name'], json['hand_size']), json['game_name']


@bp.route('/players', methods=['POST'])
def players():
    db = get_db()
    repo = get_repo()
    response = None

    if request.method == 'POST':
        player_json = request.get_json()
        for attribute in ['name', 'game_name']:
            if attribute not in player_json.keys():
                response = ({'error': f'Player {attribute} is required.'}, 401)

        if response is None:
            player, game_name = deserialize_player(player_json)
            [game] = [g for g in repo.list() if g.name == game_name]
            game.players.append(player)
            db.commit()
            response = (serialize_player(player), 201)

    return response
