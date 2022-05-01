from __future__ import annotations

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

    def known_holding_status(self, card: Card):
        if card in self.known_cards_held:
            return "Yes"
        if card in self.known_cards_not_held:
            return "No"
        return "Maybe"

    def has(self, card: Card, game: Game):
        if self.known_holding_status(card) == "Maybe":
            self.known_cards_held.append(card)
            em.emit('has', game=game, player=self, card=card)

    def lacks(self, card: Card, game: Game):
        if self.known_holding_status(card) == "Maybe":
            self.known_cards_not_held.append(card)
            em.emit('lacks', game=game, player=self, card=card)

    def shows(self, cardset: Set[Card], game: Game):
        self.shown_cardsets.append(cardset)
        em.emit('shown', game=game, player=self)


class Game:
    def __init__(self, name: str, cards: List[Card], players: List[Player]):
        self.name = name
        self.cards = cards
        self.players = players
        self.confidential_file: Set[Card] = set()

    def card_list(self, card_type: str):
        return [card for card in self.cards if card.card_type == card_type]

    def observe_pass(self, player: Player, cardset: Set[Card]):
        for card in cardset:
            player.lacks(card, self)

    def observe_shown(self, player: Player, cardset: Set[Card]):
        player.shows(cardset, self)

    def observe_has(self, player: Player, card: Card):
        player.has(card, self)

    def known_to_be_in_a_players_hand(self, card: Card):
        for player in self.players:
            if card in player.known_cards_held:
                return True
        return False


@events.on(emitter=em, event='shown')
@events.on(emitter=em, event='lacks')
def resolve_show_elimination_rule(
    game: Game,
    player: Player,
    card: Optional[Card] = None
):
    for cardset in player.shown_cardsets:
        possible_cards = [c for c in cardset if
                          c not in player.known_cards_not_held]
        if len(possible_cards) == 1:
            player.has(possible_cards.pop(), game)


@events.on(emitter=em, event='lacks')
def resolve_at_least_one_holder_rule(
    game: Game,
    card: Card,
    player: Optional[Player] = None
):
    for player in game.players:
        if card not in player.known_cards_not_held:
            return
    game.confidential_file.add(card)


@events.on(emitter=em, event='has')
def resolve_at_most_one_holder_rule(
    game: Game,
    player: Player,
    card: Card
):
    if card in player.known_cards_held:
        for p in set(game.players) - {player}:
            p.lacks(card, game)


@events.on(emitter=em, event='has')
def resolve_file_has_a_full_set_rule(
    game: Game,
    card: Card,
    player: Optional[Player] = None
):
    unlocated_cards = [c for c in game.card_list(card.card_type) if
                       not game.known_to_be_in_a_players_hand(c)]
    if len(unlocated_cards) == 1:
        game.confidential_file.add(unlocated_cards.pop())


@events.on(emitter=em, event='has')
@events.on(emitter=em, event='lacks')
def resolve_hand_size_rule(
    game: Game,
    player: Player,
    card: Optional[Card] = None
):
    cards_having = [c for c in game.cards if c in player.known_cards_held]
    cards_lacking = [c for c in game.cards if c in player.known_cards_not_held]

    if len(cards_having) == player.hand_size:
        for c in set(game.cards) - set(cards_having):
            player.lacks(c, game)
    elif len(game.cards) - len(cards_lacking) == player.hand_size:
        for c in set(game.cards) - set(cards_lacking):
            player.has(c, game)
