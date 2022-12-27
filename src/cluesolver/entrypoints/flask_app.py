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
    game = cluegame.Game(request.json["name"])
    repo.add(game)
    session.commit()
    return {"name": game.name}, 201


@app.route("/games/<game_name>", methods=["GET"])
def get_game(game_name):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    try:
        game = repo.get(escape(game_name))
    except NoResultFound as e:
        return {"message": str(e)}, 404
    return {"name": game.name}
