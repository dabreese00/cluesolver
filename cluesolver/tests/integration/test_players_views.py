import pytest


PLAYERS_PATH = '/players'


@pytest.fixture
def player_dict():
    return {
        'name': 'Benji',
        'hand_size': 3,
    }


def post_player(client, json):
    return client.post(PLAYERS_PATH, json=json)


def get_player(client, name):
    return client.get(PLAYERS_PATH + '/' + name)


# def test_create_player(app, client, player_dict):
#     r1 = post_player(client, player_dict)
#     assert r1.status_code == 201
#     r2 = client.get(PLAYERS_PATH)
#     players = r2.json['players']
#     assert len(players) == 1
#     r3 = get_player(client, players[0]['name'])
#     assert r3.status_code == 200
#
#
# def test_create_player_returns_401_if_noname(app, client, player_dict):
#     player_dict.pop('name')
#     r = post_player(client, player_dict)
#     assert r.status_code == 401
#
#
# def test_create_player_twice_returns_401(app, client, player_dict):
#     r1 = post_player(client, player_dict)
#     assert r1.status_code == 201
#     r2 = post_player(client, player_dict)
#     assert r2.status_code == 401
#
#
# def test_get_nonexistent_player_returns_404(app, client):
#     r = get_player(client, 'idontexist')
#     assert r.status_code == 404
