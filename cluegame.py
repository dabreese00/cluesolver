from dataclasses import dataclass
from functools import partial


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
                self._on_lacks(fact.player, c)

        elif fact.fact_type == "Show":
            self._on_shown(fact.player, fact.cardset)

        elif fact.fact_type == "Has":
            self._on_has(fact.player, fact.card)

    def _on_lacks(self, player, card):
        if self.has[(player, card)] == "Maybe":
            self.has[(player, card)] = "No"
            self.resolve_at_least_one_holder_rule(card)
            self.resolve_show_elimination_rule(player)
            self.resolve_minimum_hand_size_rule(player)

    def _on_shown(self, player, cardset):
        self.shown_by[player].append(cardset)
        self.resolve_show_elimination_rule(player)

    def _on_has(self, player, card):
        if self.has[(player, card)] == "Maybe":
            self.has[(player, card)] = "Yes"
            self.resolve_at_most_one_holder_rule(player, card)
            self.resolve_file_has_a_full_set_rule(card.card_type)
            self.resolve_maximum_hand_size_rule(player)

    def resolve_show_elimination_rule(self, player):
        for cardset in self.shown_by[player]:
            only_possible_card = filter_to_singleton(cardset,
                                                partial(self._definitely_lacks, player))
            if only_possible_card:
                self._on_has(player, only_possible_card)

    def resolve_at_least_one_holder_rule(self, card):
        for player in self.players:
            if not self._definitely_lacks(player, card):
                return
        self.confidential_file.add(card)

    def resolve_at_most_one_holder_rule(self, player, card):
        if self._definitely_has(player, card):
            for p in set(self.players) - {player}:
                self._on_lacks(p, card)

    def resolve_file_has_a_full_set_rule(self, card_type):
        only_unlocated_card = filter_to_singleton(self.card_list(card_type),
                                             self._known_to_be_in_a_players_hand)
        if only_unlocated_card:
            self.confidential_file.add(only_unlocated_card)

    def resolve_maximum_hand_size_rule(self, player):
        cards_in_hand = []
        for c in self.cards:
            if self._definitely_has(player, c):
                cards_in_hand.append(c)
        if len(cards_in_hand) == player.hand_size:
            for c in set(self.cards) - set(cards_in_hand):
                self._on_lacks(player, c)

    def resolve_minimum_hand_size_rule(self, player):
        cards_not_in_hand = []
        for c in self.cards:
            if self._definitely_lacks(player, c):
                cards_not_in_hand.append(c)
        if len(cards_not_in_hand) == len(self.cards) - player.hand_size:
            for c in set(self.cards) - set(cards_not_in_hand):
                self._on_has(player, c)

    def _known_to_be_in_a_players_hand(self, card):
        for p in self.players:
            if self._definitely_has(p, card):
                return True
        return False

    def _definitely_has(self, player, card):
        return self.has[(player, card)] == "Yes"

    def _definitely_lacks(self, player, card):
        return self.has[(player, card)] == "No"


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
