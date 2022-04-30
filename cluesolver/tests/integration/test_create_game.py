def test_create_game(app, client):
    games_path = '/games'
    game_dict = {
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
    r1 = client.post(games_path, json=game_dict)
    print(r1.json)
    assert r1.status_code == 201

    r2 = client.get(games_path)
    assert r2.status_code == 200
    assert len(r2.json['games']) == 1

    game_received = r2.json['games'][0]
    r3 = client.get(games_path + '/' + game_received['name'])
    assert r3.status_code == 200
