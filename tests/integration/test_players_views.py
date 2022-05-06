import pytest
from sqlalchemy import select

from cluesolver.domain.cluegame import Player
from cluesolver.adapters.db import get_db, get_repo


def insert_game(session, name):
    session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': name}
    )
    [[game_id]] = session.execute(
        "SELECT id FROM game WHERE name=:name", {'name': name}
    )
    return game_id


@pytest.fixture
def app_db_with_added_game(app):
    with app.app_context():
        db = get_db()
        repo = get_repo()
        insert_game(db, "game1")
        db.commit()
        game = repo.get("game1")
        return repo, game


@pytest.fixture
def post_dict(app_db_with_added_game):
    _, game = app_db_with_added_game
    return {
        'name': 'player1',
        'game_name': game.name,
        'hand_size': 3
    }


relative_url = '/players'

model = Player

# list_key = 'players'


def post(client, json):
    return client.post(relative_url, json=json)


# def get_detail(client, name):
#     return client.get(relative_url + '/' + name)


# def get(client):
#     return client.get(relative_url)


def list_via_direct_query(app):
    with app.app_context():
        db = get_db()
        sel = select(model.name)
        objects = list(db.execute(sel).fetchall())
    return objects


# def create_via_direct_query(app, obj_dict):
#     with app.app_context():
#         db = get_db()
#         ins = insert(model)
#         result = db.execute(ins, obj_dict)
#         db.commit()
#     return result


def test_create(app, client, post_dict):
    r = post(client, post_dict)
    assert r.status_code == 201

    objects = list_via_direct_query(app)
    assert objects == [(post_dict['name'],)]


# def test_list(app, client, post_dict):
#     create_via_direct_query(app, post_dict)
#     response = get(client)
#     objects = response.json[list_key]
#     assert response.status_code == 200
#     assert objects == [post_dict]


def test_create_returns_401_if_noname(app, client, post_dict):
    temp_post_dict = post_dict.copy()
    temp_post_dict.pop('name')
    r = post(client, temp_post_dict)
    assert r.status_code == 401
