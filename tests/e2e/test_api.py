import uuid
import requests
import pytest

from cluesolver.config import get_api_url


def random_name():
    return str(uuid.uuid1())


@pytest.mark.usefixtures('postgres_session')
def test_api_post_returns_game():
    game_name = random_name()
    url = get_api_url()

    r = requests.post(f"{url}/games", json={'name': game_name})

    assert r.status_code == 201
    assert r.json()['name'] == game_name


def test_api_post_game_is_saved(postgres_session):
    game_name = random_name()
    url = get_api_url()

    requests.post(f"{url}/games", json={'name': game_name})

    [[name]] = postgres_session.execute(
        "SELECT name FROM game WHERE name=:name", {'name': game_name}
    )

    assert name == game_name


def test_api_post_onto_single_game_returns_error(postgres_session):
    game_name = random_name()
    url = get_api_url()

    postgres_session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': game_name}
    )
    postgres_session.commit()

    r = requests.post(f"{url}/games/{game_name}", json={'name': game_name})

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


def test_api_returns_single_game(postgres_session):
    game_name = "abc"
    url = get_api_url()

    postgres_session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': game_name}
    )
    postgres_session.commit()

    r = requests.get(f"{url}/games/{game_name}")

    assert r.status_code == 200
    assert r.json()['name'] == game_name


@pytest.mark.xfail
def test_api_deletes_game(postgres_session):
    game_name = random_name()
    url = get_api_url()

    postgres_session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': game_name}
    )
    postgres_session.commit()

    r = requests.delete(f"{url}/games/{game_name}")

    assert r.status_code == 204

    games = postgres_session.execute(
        "SELECT id FROM game WHERE name = :name", {'name': game_name}
    )

    assert len(games) == 0
