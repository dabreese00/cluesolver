from cluegame import Game, Card, Player, PassFact, ShowFact, HasFact
import pytest


@pytest.fixture
def single_cardset_game():
    cards = [Card("Joe", "Person"), Card("Rope", "Weapon"),
             Card("Kitchen", "Room")]
    players = [Player("Bob", 3)]
    return Game(cards, players)


@pytest.fixture
def two_person_cards():
    return [Card("Joe", "Person"), Card("Jim", "Person")]


@pytest.fixture
def weapon_card_and_room_card():
    return [Card("Rope", "Weapon"), Card("Kitchen", "Room")]


@pytest.fixture
def four_cards(two_person_cards, weapon_card_and_room_card):
    return two_person_cards + weapon_card_and_room_card


@pytest.fixture
def player():
    return Player("Bob", 3)


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


def test_observing_a_show_with_two_unheld_cards_marks_final_has(
        four_cards, player):
    cards = four_cards
    player = Player("Bob", 3)
    g = Game(cards, [player])

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


def test_observing_show_me_marks_card_held(player):
    card = Card("Joe", "Person")
    g = Game([card], [player])

    obs = HasFact(player, card)
    g.make_observation(obs)

    assert g.has[(player, card)] == "Yes"


def test_observing_show_me_marks_card_not_held_by_others():
    card = Card("Joe", "Person")
    players = [Player("Bob", 3),
               Player("Riccha", 3),
               Player("Fergie", 3)]
    g = Game([card], players)

    obs = HasFact(players[0], card)
    g.make_observation(obs)

    for p in players[1:]:
        assert g.has[(p, card)] == "No"


def test_observing_pass_with_show_and_unheld_card_marks_final_has(
        four_cards, player):
    cards = four_cards
    g = Game(cards, [player])

    g.has[(player, cards[0])] = "No"
    show_obs = ShowFact(player, set(cards[1:]))
    g.make_observation(show_obs)

    assert g.has[(player, cards[3])] == "Maybe"

    pass_obs = PassFact(player, set(cards[:3]))
    g.make_observation(pass_obs)

    assert g.has[(player, cards[3])] == "Yes"


def test_observing_last_has_of_card_type_marks_confidential_file(
        two_person_cards, weapon_card_and_room_card):
    player = Player("Bob", 3)
    g = Game(two_person_cards + weapon_card_and_room_card, [player])

    has_obs = HasFact(player, two_person_cards[0])
    g.make_observation(has_obs)

    assert two_person_cards[1] in g.confidential_file


def test_observing_has_at_players_hand_size_marks_remaining_lacks(four_cards):
    cards = four_cards
    player = Player("Bob", 2)
    g = Game(cards, [player])
    has_obs_first = HasFact(player, cards[0])
    has_obs_second = HasFact(player, cards[1])

    g.make_observation(has_obs_first)

    assert g.has[(player, cards[2])] == "Maybe"
    assert g.has[(player, cards[3])] == "Maybe"

    g.make_observation(has_obs_second)

    assert g.has[(player, cards[2])] == "No"
    assert g.has[(player, cards[3])] == "No"


def test_observing_lacks_at_players_hand_size_marks_remaining_has(four_cards):
    cards = four_cards
    cards.append(Card("Knife", "Weapon"))
    player = Player("Bob", 2)
    g = Game(cards, [player])
    pass_obs = PassFact(player, cards[:3])

    g.make_observation(pass_obs)

    assert g.has[(player, cards[3])] == "Yes"
    assert g.has[(player, cards[4])] == "Yes"
