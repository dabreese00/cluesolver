from cluegame import Game, Card, Player
import pytest


@pytest.fixture
def person_card():
    return Card("Joe", "Person")


@pytest.fixture
def weapon_card():
    return Card("Rope", "Weapon")


@pytest.fixture
def room_card():
    return Card("Kitchen", "Room")


@pytest.fixture
def basic_card_list():
    return [
        Card("Joe", "Person"),
        Card("Jim", "Person"),
        Card("Janet", "Person"),
        Card("Jamie", "Person"),
        Card("Rope", "Weapon"),
        Card("Knife", "Weapon"),
        Card("Lead Pipe", "Weapon"),
        Card("Candlestick", "Weapon"),
        Card("Kitchen", "Room"),
        Card("Lounge", "Room"),
        Card("Study", "Room"),
        Card("Billiard Room", "Room"),
    ]


@pytest.fixture
def two_person_cards(person_card):
    return [person_card, Card("Jim", "Person")]


@pytest.fixture
def basic_player_list():
    return [
        Player("Bob", 3),
        Player("Riccha", 3),
        Player("Fergie", 3),
        Player("Khalid", 3),
    ]


@pytest.fixture
def single_cardset_game(person_card, weapon_card, room_card, player):
    return Game([person_card, weapon_card, room_card], [player])


@pytest.fixture
def basic_game(basic_card_list, basic_player_list):
    return Game(basic_card_list, basic_player_list)


def test_card_list_filters_by_type(person_card, weapon_card, room_card):
    cards = [person_card, weapon_card]
    g = Game(cards, [])

    assert g.card_list("Person") == [person_card]


def test_observing_a_pass_records_cards_not_held(basic_game):
    g = basic_game
    player = g.players[0]
    cardset = {
        g.card_list("Person")[0],
        g.card_list("Weapon")[0],
        g.card_list("Room")[0],
    }

    g.observe_pass(player, cardset)

    for card in cardset:
        assert g.has[(player, card)] == "No"


def test_observing_a_show_records_cardset_shown_by(basic_game):
    g = basic_game
    player = g.players[0]
    cardset = {
        g.card_list("Person")[0],
        g.card_list("Weapon")[0],
        g.card_list("Room")[0],
    }

    g.observe_shown(player, cardset)

    assert cardset in g.shown_by[player]


def test_observing_a_show_with_two_unheld_cards_marks_final_has(basic_game):
    g = basic_game
    cards = g.cards
    player = g.players[0]

    g.observe_pass(player, set(cards[:3]))
    g.observe_shown(player, set(cards[1:4]))

    assert g.has[(player, cards[3])] == "Yes"


def test_observing_final_pass_marks_confidential_file(basic_game):
    g = basic_game
    player = g.players[0]
    cardset = {
        g.card_list("Person")[0],
        g.card_list("Weapon")[0],
        g.card_list("Room")[0],
    }

    for p in set(g.players) - {player}:
        g.observe_pass(p, cardset)

    assert set() == set(g.confidential_file)

    g.observe_pass(player, cardset)

    assert cardset == set(g.confidential_file)


def test_observing_has_gets_recorded(basic_game):
    g = basic_game
    card = g.cards[0]
    player = g.players[0]

    g.observe_has(player, card)

    assert g.has[(player, card)] == "Yes"


def test_observing_has_marks_card_not_held_by_others(basic_game):
    g = basic_game
    card = g.cards[0]

    g.observe_has(g.players[0], card)

    for p in g.players[1:]:
        assert g.has[(p, card)] == "No"


def test_observing_pass_with_show_and_unheld_card_marks_final_has(basic_game):
    g = basic_game
    cards = g.cards[:4]
    player = g.players[0]
    g.has[(player, cards[0])] = "No"

    g.observe_shown(player, set(cards[1:]))

    assert g.has[(player, cards[3])] == "Maybe"

    g.observe_pass(player, set(cards[:3]))

    assert g.has[(player, cards[3])] == "Yes"


def test_observing_last_has_of_card_type_marks_confidential_file(
        two_person_cards):
    player = Player("Bob", 3)
    g = Game(two_person_cards, [player])

    g.observe_has(player, two_person_cards[0])

    assert two_person_cards[1] in g.confidential_file


def test_observing_has_at_players_hand_size_marks_remaining_lacks(basic_game):
    g = basic_game
    cards = g.cards
    player = g.players[0]

    g.observe_has(player, cards[0])
    g.observe_has(player, cards[1])

    assert g.has[(player, cards[3])] == "Maybe"
    assert g.has[(player, cards[4])] == "Maybe"

    g.observe_has(player, cards[2])

    assert g.has[(player, cards[3])] == "No"
    assert g.has[(player, cards[4])] == "No"


def test_observing_lacks_at_players_hand_size_marks_remaining_has(basic_game):
    g = basic_game
    cards = g.cards
    player = g.players[0]

    g.observe_pass(player, cards[:3])
    g.observe_pass(player, cards[3:6])
    g.observe_pass(player, cards[6:9])

    for c in cards[9:12]:
        assert g.has[(player, c)] == "Yes"
