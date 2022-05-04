import pytest

from cluesolver.cluegame import Player


@pytest.fixture
def player():
    return Player("Riccha", 3)


def test_constructor_with_hand_size(player):
    assert player.name == "Riccha"
    assert player.hand_size == 3


def test_constructor_without_hand_size():
    player = Player("Bob")
    assert player.name == "Bob"


def test_hand_size_doesnt_affect_equality(player):
    player2 = Player("Riccha", 4)
    player3 = Player("Riccha")
    assert player == player2
    assert player == player3
    assert len({player, player2, player3}) == 1


def test_equality_with_different_type(player):
    assert player != {}
