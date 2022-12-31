import uuid
import requests
import pytest
from random import randrange

from cluesolver.config import get_api_url


def random_name():
    return str(uuid.uuid1())


def random_card_dict():
    return {'name': random_name(), 'card_type': random_name()}


def random_player_dict():
    return {'name': random_name(), 'hand_size': randrange(9)}


@pytest.fixture
def game_in_database(postgres_session):
    game_name = random_name()
    postgres_session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': game_name}
    )
    postgres_session.commit()
    return game_name


@pytest.mark.usefixtures('postgres_session')
def test_api_post_returns_game():
    game_name = random_name()
    url = get_api_url()

    r = requests.post(f"{url}/games", json={'name': game_name})

    assert r.status_code == 201
    assert r.json()['name'] == game_name


@pytest.mark.usefixtures('postgres_session')
def test_api_post_game_is_saved():
    game_name = random_name()
    url = get_api_url()

    r1 = requests.post(f"{url}/games", json={'name': game_name})
    r2 = requests.post(f"{url}/games", json={'name': game_name})

    assert r1.status_code == 201
    assert r2.status_code == 204


def test_api_post_onto_single_game_returns_error(game_in_database):
    url = get_api_url()

    r = requests.post(f"{url}/games/{game_in_database}",
                      json={'name': game_in_database})

    assert r.status_code == 405


def test_api_get_returns_games(postgres_session):
    game_name = random_name()
    game_name_two = random_name()
    url = get_api_url()

    postgres_session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': game_name}
    )
    postgres_session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': game_name_two}
    )
    postgres_session.commit()

    r = requests.get(f"{url}/games")

    assert r.status_code == 200

    names = [entry['name'] for entry in r.json()]

    assert game_name in names
    assert game_name_two in names


def test_api_returns_single_game(game_in_database):
    url = get_api_url()

    r = requests.get(f"{url}/games/{game_in_database}")

    assert r.status_code == 200
    assert r.json()['name'] == game_in_database


def test_api_post_returns_card(game_in_database):
    card_json = random_card_dict()
    url = get_api_url()

    r = requests.post(f"{url}/games/{game_in_database}/cards", json=card_json)

    assert r.status_code == 201
    assert r.json()['name'] == card_json['name']
    assert r.json()['card_type'] == card_json['card_type']


@pytest.mark.usefixtures('postgres_session')
def test_api_post_card_to_nonexistent_game_returns_400():
    game_name = random_name()
    card_json = random_card_dict()
    url = get_api_url()

    r = requests.post(f"{url}/games/{game_name}/cards", json=card_json)

    assert r.status_code == 400


def test_api_post_saves_card(game_in_database):
    card_json = random_card_dict()
    url = get_api_url()

    r1 = requests.post(f"{url}/games/{game_in_database}/cards", json=card_json)
    r2 = requests.post(f"{url}/games/{game_in_database}/cards", json=card_json)

    assert r1.status_code == 201
    assert r2.status_code == 204


def test_api_post_returns_player(game_in_database):
    player_json = random_player_dict()
    url = get_api_url()

    r = requests.post(f"{url}/games/{game_in_database}/players",
                      json=player_json)

    assert r.status_code == 201
    assert r.json()['name'] == player_json['name']
    assert r.json()['hand_size'] == player_json['hand_size']


@pytest.mark.usefixtures('postgres_session')
def test_api_post_player_to_nonexistent_game_returns_400():
    game_name = random_name()
    player_json = random_player_dict()
    url = get_api_url()

    r = requests.post(f"{url}/games/{game_name}/players", json=player_json)

    assert r.status_code == 400


def test_api_post_saves_player(game_in_database):
    player_json = random_player_dict()
    url = get_api_url()

    r1 = requests.post(f"{url}/games/{game_in_database}/players",
                       json=player_json)
    r2 = requests.post(f"{url}/games/{game_in_database}/players",
                       json=player_json)

    assert r1.status_code == 201
    assert r2.status_code == 204
