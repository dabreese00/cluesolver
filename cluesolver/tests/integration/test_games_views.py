import pytest


GAMES_PATH = '/games'


@pytest.fixture
def game_dict():
    return {'name': 'Oogas'}


def post_game(client, json):
    return client.post(GAMES_PATH, json=json)


def get_game(client, name):
    return client.get(GAMES_PATH + '/' + name)


def test_create_game(app, client, game_dict):
    r1 = post_game(client, game_dict)
    assert r1.status_code == 201

    r2 = client.get(GAMES_PATH)
    assert r2.status_code == 200
    assert len(r2.json['games']) == 1

    game_received = r2.json['games'][0]
    r3 = get_game(client, game_received['name'])
    assert r3.status_code == 200


def test_create_game_returns_401_if_noname(app, client, game_dict):
    game_dict.pop('name')
    r = post_game(client, game_dict)
    assert r.status_code == 401


def test_create_game_twice_returns_401(app, client, game_dict):
    r1 = post_game(client, game_dict)
    assert r1.status_code == 201
    r2 = post_game(client, game_dict)
    assert r2.status_code == 401


def test_get_nonexistent_game_returns_404(app, client):
    r = get_game(client, 'idontexist')
    assert r.status_code == 404
