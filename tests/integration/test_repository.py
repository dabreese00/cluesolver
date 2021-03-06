import pytest
from sqlalchemy.exc import NoResultFound

from cluesolver.domain.cluegame import Game, Player, Card
from cluesolver.adapters.repository import SqlAlchemyRepository


def test_repository_can_save_a_game(session):
    game = Game("Oogas")
    repo = SqlAlchemyRepository(session)
    repo.add(game)
    session.commit()

    rows = session.execute(
        'SELECT name FROM game'
    )
    assert list(rows) == [("Oogas",)]


def insert_game(session, name):
    session.execute(
        "INSERT INTO game (name) VALUES (:name)", {'name': name}
    )
    [[game_id]] = session.execute(
        "SELECT id FROM game WHERE name=:name", {'name': name}
    )
    return game_id


def insert_player(session, game_id, name):
    session.execute(
        "INSERT INTO player (name, game_id, hand_size) "
        "VALUES (:name, :game_id, :hand_size)",
        {'name': name, 'game_id': game_id, 'hand_size': 3}
    )


def insert_card(session, game_id, name):
    session.execute(
        "INSERT INTO card (name, game_id, card_type) "
        "VALUES (:name, :game_id, :card_type)",
        {'name': name, 'game_id': game_id, 'card_type': 'Room'}
    )


def test_repository_can_retrieve_game(session):
    insert_game(session, "game1")
    insert_game(session, "game2")

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("game1")

    expected = Game("game1")
    assert retrieved == expected


def test_repository_can_list_games(session):
    insert_game(session, "game1")
    insert_game(session, "game2")

    repo = SqlAlchemyRepository(session)
    retrieved = repo.list()

    expected = [Game("game1"), Game("game2")]
    assert set(retrieved) == set(expected)  # don't test the order returned


def test_can_retrieve_player_via_game(session):
    game1_id = insert_game(session, "game1")
    insert_player(session, game1_id, "player1")

    repo = SqlAlchemyRepository(session)
    game_retrieved = repo.get("game1")
    [retrieved] = [p for p in game_retrieved.players
                   if p.name == "player1"]
    expected = Player("player1", 3)
    assert retrieved == expected
    assert retrieved.hand_size == expected.hand_size


def test_can_retrieve_card_via_game(session):
    game1_id = insert_game(session, "game1")
    insert_card(session, game1_id, "card1")

    repo = SqlAlchemyRepository(session)
    game_retrieved = repo.get("game1")
    [retrieved] = [c for c in game_retrieved.cards
                   if c.name == "card1"]
    expected = Card("card1", "Room")
    assert retrieved == expected
    assert retrieved.card_type == expected.card_type


@pytest.fixture
def repo_with_added_game(session):
    insert_game(session, "game1")
    repo = SqlAlchemyRepository(session)
    game = repo.get("game1")
    return repo, game


def test_can_save_player_via_game(session, repo_with_added_game):
    repo, game = repo_with_added_game

    game.players.append(Player("player1", 3))
    repo.add(game)
    session.commit()

    rows = session.execute("SELECT name, hand_size FROM player")

    assert list(rows) == [("player1", 3)]


def test_can_save_card_via_game(session, repo_with_added_game):
    repo, game = repo_with_added_game

    game.cards.append(Card("card1", "Room"))
    repo.add(game)
    session.commit()

    rows = session.execute("SELECT name, card_type FROM card")

    assert list(rows) == [("card1", "Room")]


def test_add_updates_existing_game(session, repo_with_added_game):
    repo, game = repo_with_added_game

    game.cards.append(Card("card1", "Room"))
    repo.add(game)
    session.commit()

    rows = session.execute("SELECT name FROM game")

    assert list(rows) == [("game1",)]


def test_get_nonexistent_game_throws_noresultfound(session):
    insert_game(session, "game1")
    repo = SqlAlchemyRepository(session)
    with pytest.raises(NoResultFound):
        repo.get("game2")
