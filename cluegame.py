from dataclasses import dataclass


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
        self.has[(player, card)] = "No"
        self.resolve_at_least_one_holder_rule(card)

    def _on_shown(self, player, cardset):
        self.shown_by[player].append(cardset)
        self.resolve_show_elimination_rule(player)

    def _on_has(self, player, card):
        self.has[(player, card)] = "Yes"

    def resolve_show_elimination_rule(self, player):
        for cardset in self.shown_by[player]:
            possible_cards = set(cardset)
            for c in cardset:
                if self._definitely_lacks(player, c):
                    possible_cards.remove(c)
            if len(possible_cards) == 1:
                self._on_has(player, *possible_cards)

    def resolve_at_least_one_holder_rule(self, card):
        for player in self.players:
            if not self._definitely_lacks(player, card):
                return
        self.confidential_file.add(card)

    def _definitely_has(self, player, card):
        return self.has[(player, card)] == "Yes"

    def _definitely_lacks(self, player, card):
        return self.has[(player, card)] == "No"


@dataclass(frozen=True)
class Card:
    name: str
    card_type: str


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
