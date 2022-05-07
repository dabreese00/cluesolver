import uuid
import requests

from cluesolver.config import get_api_url


def random_name():
    return str(uuid.uuid1())


def test_api_returns_game(postgres_session):
    game_name = random_name()
    url = get_api_url()

    r = requests.post(f"{url}/games", json={'name': game_name})

    [[name]] = postgres_session.execute(
        "SELECT name FROM game"
    )

    assert r.status_code == 201
    assert r.json()['name'] == game_name
    assert name == game_name

# @pytest.fixture
# def add_game(postgres_session):
#     games_added = set()
#     players_added = set()
#     cards_added = set()
#
#     def _add_game(game_name, player_name, card_name):
#         postgres_session.execute(
#             "INSERT INTO game (name) VALUES (:name)", {'name': game_name}
#         )
#         [[game_id]] = postgres_session.execute(
#             "SELECT id FROM game WHERE name = :name", {'name': game_name}
#         )
#         postgres_session.execute(
#             "INSERT INTO player (name, game_id, hand_size) "
#             "VALUES (:name, :game_id, :hand_size)",
#             {'name': player_name, 'game_id': game_id, 'hand_size': 3}
#         )
#         postgres_session.execute(
#             "INSERT INTO card (name, game_id, card_type) "
#             "VALUES (:name, :game_id, :card_type)",
#             {'name': card_name, 'game_id': game_id, 'card_type': 'Room'}
#         )
#         games_added.add(game_name)
#         players_added.add(player_name)
#         cards_added.add(card_name)
#         postgres_session.commit()
#
#     yield _add_game
#
#     for game_name in games_added:
#         postgres_session.execute(
#             "DELETE FROM game WHERE name = :name", {'name': game_name}
#         )
#     for player_name in players_added:
#         postgres_session.execute(
#             "DELETE FROM player WHERE name = :name", {'name': player_name}
#         )
#     for card_name in cards_added:
#         postgres_session.execute(
#             "DELETE FROM card WHERE name = :name", {'name': card_name}
#         )
