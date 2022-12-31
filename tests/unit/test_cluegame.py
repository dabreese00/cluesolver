from cluesolver.domain.cluegame import (
    Card, Player, list_cards_by_type, calculate_deductions
)
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
def one_player(basic_player_list):
    return basic_player_list[0]


@pytest.fixture
def one_cardset(basic_card_list):
    cardset = {
        basic_card_list[0],
        basic_card_list[4],
        basic_card_list[8],
    }
    return cardset


def test_list_cards_by_type(person_card, weapon_card):
    cards = [person_card, weapon_card]
    assert list_cards_by_type(cards, "Person") == [person_card]


def test_observing_a_pass_records_cards_not_held(
    one_cardset, one_player
):
    one_player.passes(one_cardset)
    for card in one_cardset:
        assert card in one_player.known_cards_not_held


def test_observing_a_show_records_cardset_shown_by(
    one_cardset, one_player
):
    one_player.shows(one_cardset)
    assert one_cardset in one_player.shown_cardsets


def test_calculate_show_with_two_unheld_cards(
    basic_card_list, one_player
):
    cards = basic_card_list
    one_player.passes(set(cards[:3]))
    one_player.shows(set(cards[1:4]))
    calculate_deductions([one_player], cards, [])
    assert cards[3] in one_player.known_cards_held


def test_calculate_observing_final_pass_of_a_card(
    one_cardset, one_player, basic_player_list, basic_card_list
):
    for p in set(basic_player_list) - {one_player}:
        p.passes(one_cardset)
    cf = calculate_deductions(basic_player_list, basic_card_list, [])
    assert set() == set(cf)

    one_player.passes(one_cardset)
    cf = calculate_deductions(basic_player_list, basic_card_list, [])
    assert set(one_cardset) == set(cf)


def test_observing_has_gets_recorded(
    person_card, one_player
):
    one_player.has(person_card)
    assert person_card in one_player.known_cards_held


def test_calculate_observing_has(
    person_card, one_player, basic_player_list
):
    one_player.has(person_card)
    calculate_deductions(basic_player_list, [person_card], [])
    other_players = set(basic_player_list) - {one_player}
    for p in other_players:
        assert person_card in p.known_cards_not_held


def test_calculate_observing_pass_with_show_and_unheld_card(
    basic_card_list, one_player
):
    cards = basic_card_list[:4]
    one_player.known_cards_not_held.append(cards[0])
    one_player.shows(set(cards[1:]))
    calculate_deductions([one_player], basic_card_list, [])
    assert cards[3] not in (one_player.known_cards_held +
                            one_player.known_cards_not_held)
    one_player.passes(set(cards[:3]))
    calculate_deductions([one_player], basic_card_list, [])
    assert cards[3] in one_player.known_cards_held


def test_calculate_observing_last_has_of_card_type(
    two_person_cards, one_player
):
    one_player.has(two_person_cards[0])
    cf = calculate_deductions([one_player], two_person_cards, [])
    assert two_person_cards[1] in cf


def test_calculate_observing_has_at_players_hand_size(
    basic_card_list, one_player
):
    one_player.has(basic_card_list[0])
    one_player.has(basic_card_list[1])
    calculate_deductions([one_player], basic_card_list, [])
    assert basic_card_list[3] not in (one_player.known_cards_held +
                                      one_player.known_cards_not_held)
    assert basic_card_list[4] not in (one_player.known_cards_held +
                                      one_player.known_cards_not_held)
    one_player.has(basic_card_list[2])
    calculate_deductions([one_player], basic_card_list, [])
    assert basic_card_list[3] in one_player.known_cards_not_held
    assert basic_card_list[4] in one_player.known_cards_not_held


def test_calculate_observing_lacks_at_players_hand_size(
    basic_card_list, one_player
):
    one_player.passes(basic_card_list[:3])
    one_player.passes(basic_card_list[3:6])
    one_player.passes(basic_card_list[6:9])
    calculate_deductions([one_player], basic_card_list, [])
    for c in basic_card_list[9:12]:
        assert c in one_player.known_cards_held
