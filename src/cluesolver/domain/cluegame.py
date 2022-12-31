from typing import List, Set, Optional
from dataclasses import dataclass

import event_emitter as events


em = events.EventEmitter()


@dataclass(unsafe_hash=True)
class Card:
    name: str
    card_type: str


class Player:
    def __init__(self, name: str, hand_size: Optional[int] = None):
        self.name = name
        self.hand_size = hand_size
        self.known_cards_held: List[Card] = []
        self.known_cards_not_held: List[Card] = []
        self.shown_cardsets: List[Set[Card]] = []

    def __eq__(self, other):
        if isinstance(other, Player):
            return other.name == self.name
        return NotImplemented

    def __hash__(self):
        return hash(self.name)

    def has(self, card: Card):
        if card not in self.known_cards_held + self.known_cards_not_held:
            self.known_cards_held.append(card)

    def lacks(self, card: Card):
        if card not in self.known_cards_held + self.known_cards_not_held:
            self.known_cards_not_held.append(card)

    def shows(self, cardset: Set[Card]):
        self.shown_cardsets.append(cardset)

    def passes(self, cardset: Set[Card]):
        for card in cardset:
            self.lacks(card)


def is_known_to_be_in_a_players_hand(players, card):
    for player in players:
        if card in player.known_cards_held:
            return True
    return False


def list_cards_by_type(cards, card_type):
    return [card for card in cards if card.card_type == card_type]


def calculate_deductions(players, cards, confidential_file):
    confidential_file = set()
    for player in players:
        for card in player.known_cards_held:
            em.emit(
                'has', players=players, cards=cards,
                confidential_file=confidential_file,
                player=player, card=card
            )
        for card in player.known_cards_not_held:
            em.emit(
                'lacks', players=players, cards=cards,
                confidential_file=confidential_file,
                player=player, card=card
            )
        for cardset in player.shown_cardsets:
            em.emit(
                'shown', players=players, cards=cards,
                confidential_file=confidential_file,
                player=player
            )
    return confidential_file


@events.on(emitter=em, event='shown')
@events.on(emitter=em, event='lacks')
def resolve_show_elimination_rule(
    players, cards, confidential_file,
    player: Player,
    card: Optional[Card] = None
):
    for cardset in player.shown_cardsets:
        possible_cards = [c for c in cardset if
                          c not in player.known_cards_not_held]
        if len(possible_cards) == 1:
            player.has(possible_cards.pop())


@events.on(emitter=em, event='lacks')
def resolve_at_least_one_holder_rule(
    players, cards, confidential_file,
    card: Card,
    player: Optional[Player] = None
):
    for player in players:
        if card not in player.known_cards_not_held:
            return
    confidential_file.add(card)


@events.on(emitter=em, event='has')
def resolve_at_most_one_holder_rule(
    players, cards, confidential_file,
    player: Player,
    card: Card
):
    if card in player.known_cards_held:
        for p in set(players) - {player}:
            p.lacks(card)


@events.on(emitter=em, event='has')
def resolve_file_has_a_full_set_rule(
    players, cards, confidential_file,
    card: Card,
    player: Optional[Player] = None
):
    unlocated_cards = [c for c in list_cards_by_type(cards, card.card_type) if
                       not is_known_to_be_in_a_players_hand(players, c)]
    if len(unlocated_cards) == 1:
        confidential_file.add(unlocated_cards.pop())


@events.on(emitter=em, event='has')
@events.on(emitter=em, event='lacks')
def resolve_hand_size_rule(
    players, cards, confidential_file,
    player: Player,
    card: Optional[Card] = None
):
    cards_having = [c for c in cards if c in player.known_cards_held]
    cards_lacking = [c for c in cards if c in player.known_cards_not_held]

    if len(cards_having) == player.hand_size:
        for c in set(cards) - set(cards_having):
            player.lacks(c)
    elif len(cards) - len(cards_lacking) == player.hand_size:
        for c in set(cards) - set(cards_lacking):
            player.has(c)
