from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import cluesolver.config as config
import cluesolver.domain.cluegame as cluegame
import cluesolver.adapters.orm as orm
import cluesolver.adapters.repository as repository


orm.map_orm()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/games", methods=["POST"])
def games_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    game = cluegame.Game(request.json["name"])
    repo.add(game)
    session.commit()
    return {"name": game.name}, 201
