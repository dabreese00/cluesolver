import requests


BASE_URL = 'http://127.0.0.1:5000'


def test_create_game():
    game_dict = {
        'name': 'Ooga',
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
    r1 = requests.post(BASE_URL + '/games', data=game_dict)
    assert r1.status_code == 201

    r2 = requests.get(BASE_URL + '/games')
    assert r2.status_code == 200
    assert len(r2.json()) == 1

    game_received = r2.json()[0]
    r3 = requests.get(BASE_URL + '/games/' + game_received['id'])
    assert r3.status_code == 200
