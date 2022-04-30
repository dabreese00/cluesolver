import pytest


@pytest.fixture
def game_dict():
    return {
        'name': 'Oogas',
        'players': [
            {
                'name': 'Marie',
                'hand_size': 3,
            },
            {
                'name': 'Jim',
            },
        ],
        'cards': [
            {
                'name': 'Rope',
                'type': 'Weapon',
            },
            {
                'name': 'Ballroom',
                'type': 'Room',
            },
        ],
    }


def test_create_game(app, client, game_dict):
    games_path = '/games'
    r1 = client.post(games_path, json=game_dict)
    assert r1.status_code == 201

    r2 = client.get(games_path)
    assert r2.status_code == 200
    assert len(r2.json['games']) == 1

    game_received = r2.json['games'][0]
    r3 = client.get(games_path + '/' + game_received['name'])
    assert r3.status_code == 200


def test_returns_401_if_noname(app, client, game_dict):
    games_path = '/games'
    game_dict.pop('name')
    r = client.post(games_path, json=game_dict)
    assert r.status_code == 401


def test_create_game_twice_returns_401(app, client, game_dict):
    games_path = '/games'
    r1 = client.post(games_path, json=game_dict)
    assert r1.status_code == 201
    r2 = client.post(games_path, json=game_dict)
    assert r2.status_code == 401
