from cluesolver.domain.cluegame import Game, Card, Player
from cluesolver.adapters.repository import AbstractRepository


def add_game(name: str, repo: AbstractRepository, session) -> None:
    repo.add(Game(name))
    session.commit()


def add_card(
    name: str, card_type: str, game_name: str,
    repo: AbstractRepository, session
) -> None:
    game = repo.get(game_name)
    game.cards.append(Card(name, card_type))
    session.commit()


def add_player(
    name: str, hand_size: int, game_name: str,
    repo: AbstractRepository, session
) -> None:
    game = repo.get(game_name)
    game.players.append(Player(name, hand_size))
    session.commit()
