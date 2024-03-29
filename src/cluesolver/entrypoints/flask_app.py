from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from markupsafe import escape

import cluesolver.config as config
import cluesolver.domain.cluegame as cluegame
import cluesolver.adapters.orm as orm
import cluesolver.adapters.repository as repository


orm.map_orm()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/games", methods=["POST"])
def create_game():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    games = repo.list()
    if request.json["name"] in [g.name for g in games]:
        return {}, 204
    game = cluegame.Game(request.json["name"])
    repo.add(game)
    session.commit()
    return {"name": game.name}, 201


@app.route("/games", methods=["GET"])
def list_games():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    games = [{"name": game.name} for game in repo.list()]
    return games


@app.route("/games/<game_name>", methods=["GET"])
def get_game(game_name):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    try:
        game = repo.get(escape(game_name))
    except NoResultFound as e:
        return {"message": str(e)}, 404
    return {"name": game.name}


@app.route("/games/<game_name>/cards", methods=["POST"])
def create_card(game_name):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    games = repo.list()
    for game in games:
        if game.name == escape(game_name):
            if request.json['name'] in [c.name for c in game.cards]:
                return {}, 204
            card = cluegame.Card(
                                 name=request.json['name'],
                                 card_type=request.json['card_type'])
            game.cards.append(card)
            session.commit()
            return {'name': card.name, 'card_type': card.card_type}, 201
    return {}, 400


@app.route("/games/<game_name>/players", methods=["POST"])
def create_player(game_name):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    games = repo.list()
    for game in games:
        if game.name == escape(game_name):
            if request.json['name'] in [p.name for p in game.players]:
                return {}, 204
            player = cluegame.Player(
                                     name=request.json['name'],
                                     hand_size=request.json['hand_size'])
            game.players.append(player)
            session.commit()
            return {'name': player.name, 'hand_size': player.hand_size}, 201
    return {}, 400
