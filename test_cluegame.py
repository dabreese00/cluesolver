from cluegame import Game, Card, PassFact, ShowFact, HasFact
import pytest


@pytest.fixture
def single_cardset_game():
    cards = [Card("Joe", "Person"), Card("Rope", "Weapon"),
             Card("Kitchen", "Room")]
    players = ["Bob"]
    return Game(cards, players)


def test_card_list_filters_by_type():
    cards = [Card("Joe", "Person"), Card("Rope", "Weapon")]
    players = []
    g = Game(cards, players)

    assert g.card_list("Person") == [Card("Joe", "Person")]


def test_observing_a_pass_records_cards_not_held(single_cardset_game):
    g = single_cardset_game

    player = g.players[0]
    cardset = set(g.cards)
    obs = PassFact(player=player, cardset=cardset)
    g.make_observation(obs)

    for card in cardset:
        assert g.has[(player, card)] == "No"


def test_observing_a_show_records_cardset_shown_by(single_cardset_game):
    g = single_cardset_game

    player = g.players[0]
    cardset = set(g.cards)
    obs = ShowFact(player, cardset)
    g.make_observation(obs)

    assert cardset in g.shown_by[player]


def test_observing_a_show_with_two_unheld_cards_marks_final_has():
    cards = [Card("Joe", "Person"), Card("Rope", "Weapon"),
             Card("Kitchen", "Room"), Card("Jim", "Person")]
    players = ["Bob"]
    g = Game(cards, players)

    player = g.players[0]
    pass_obs = PassFact(player, set(cards[:3]))
    show_obs = ShowFact(player, set(cards[1:]))

    g.make_observation(pass_obs)
    g.make_observation(show_obs)

    assert g.has[(player, cards[3])] == "Yes"


def test_observing_a_pass_marks_confidential_file(single_cardset_game):
    g = single_cardset_game

    player = g.players[0]
    cardset = set(g.cards)
    obs = PassFact(player, cardset)
    g.make_observation(obs)

    assert set(g.cards) == set(g.confidential_file)


def test_observing_show_me_marks_card_held():
    card = Card("Joe", "Person")
    player = "Bob"
    g = Game([card], [player])

    obs = HasFact(player, card)
    g.make_observation(obs)

    assert g.has[(player, card)] == "Yes"
