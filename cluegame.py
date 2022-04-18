from dataclasses import dataclass
from functools import partial
import event_emitter as events


em = events.EventEmitter()


class Game:
    def __init__(self, cards, players):
        self.cards = cards
        self.players = players

        self.has = {}
        for player in players:
            for card in cards:
                self.has[(player, card)] = "Maybe"

        self.shown_by = {}
        for player in players:
            self.shown_by[player] = []

        self.confidential_file = set()

        self.hand_sizes = {}

    def card_list(self, card_type):
        return [card for card in self.cards if card.card_type == card_type]

    def make_observation(self, fact):
        if fact.fact_type == "Pass":
            for c in fact.cardset:
                self.update_status(fact.player, c, 'lacks')

        elif fact.fact_type == "Show":
            em.emit('shown', game=self, player=fact.player,
                    cardset=fact.cardset)

        elif fact.fact_type == "Has":
            self.update_status(fact.player, fact.card, 'has')

    def update_status(self, player, card, status):
        if self.has[(player, card)] == "Maybe":
            em.emit(status, game=self, player=player, card=card)

    def known_to_be_in_a_players_hand(self, card):
        for p in self.players:
            if self.definitely_has(p, card):
                return True
        return False

    def definitely_has(self, player, card):
        return self.has[(player, card)] == "Yes"

    def definitely_lacks(self, player, card):
        return self.has[(player, card)] == "No"


@events.on(emitter=em, event='lacks')
def mark_lack(game, player, card):
    game.has[(player, card)] = "No"


@events.on(emitter=em, event='shown')
def mark_shown(game, player, cardset):
    game.shown_by[player].append(cardset)


@events.on(emitter=em, event='has')
def mark_has(game, player, card):
    game.has[(player, card)] = "Yes"


@events.on(emitter=em, event='shown')
@events.on(emitter=em, event='lacks')
def resolve_show_elimination_rule(game, player, card=None, cardset=None):
    for cardset in game.shown_by[player]:
        only_possible_card = (
            filter_to_singleton(cardset,
                                partial(game.definitely_lacks, player)))
        if only_possible_card:
            game.update_status(player, only_possible_card, 'has')


@events.on(emitter=em, event='lacks')
def resolve_at_least_one_holder_rule(game, card, player=None):
    for player in game.players:
        if not game.definitely_lacks(player, card):
            return
    game.confidential_file.add(card)


@events.on(emitter=em, event='has')
def resolve_at_most_one_holder_rule(game, player, card):
    if game.definitely_has(player, card):
        for p in set(game.players) - {player}:
            game.update_status(p, card, 'lacks')


@events.on(emitter=em, event='has')
def resolve_file_has_a_full_set_rule(game, card, player=None):
    only_unlocated_card = (
        filter_to_singleton(game.card_list(card.card_type),
                            game.known_to_be_in_a_players_hand))
    if only_unlocated_card:
        game.confidential_file.add(only_unlocated_card)


@events.on(emitter=em, event='has')
def resolve_maximum_hand_size_rule(game, player, card=None):
    cards_in_hand = []
    for c in game.cards:
        if game.definitely_has(player, c):
            cards_in_hand.append(c)
    if len(cards_in_hand) == player.hand_size:
        for c in set(game.cards) - set(cards_in_hand):
            game.update_status(player, c, 'lacks')


@events.on(emitter=em, event='lacks')
def resolve_minimum_hand_size_rule(game, player, card=None):
    cards_not_in_hand = []
    for c in game.cards:
        if game.definitely_lacks(player, c):
            cards_not_in_hand.append(c)
    if len(cards_not_in_hand) == len(game.cards) - player.hand_size:
        for c in set(game.cards) - set(cards_not_in_hand):
            game.update_status(player, c, 'has')


def filter_to_singleton(iterable, func):
    """Given func, a boolean map on members of iterable --
    return either the only matching member, or None if not exactly one match.
    """
    possibilities = set(iterable.copy())
    for p in iterable:
        if func(p):
            possibilities.remove(p)
    if len(possibilities) == 1:
        return possibilities.pop()


@dataclass(frozen=True)
class Card:
    name: str
    card_type: str


@dataclass(frozen=True)
class Player:
    name: str
    hand_size: int


@dataclass(frozen=True)
class PassFact:
    player: str
    cardset: set
    fact_type: str = "Pass"


@dataclass(frozen=True)
class ShowFact:
    player: str
    cardset: set
    fact_type: str = "Show"


@dataclass(frozen=True)
class HasFact:
    player: str
    card: Card
    fact_type: str = "Has"
