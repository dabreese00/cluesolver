from dataclasses import dataclass
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

    def card_list(self, card_type):
        return [card for card in self.cards if card.card_type == card_type]

    def observe_pass(game, player, cardset):
        for c in cardset:
            game.update_status(player, c, 'lacks')

    def observe_shown(game, player, cardset):
        em.emit('shown', game=game, player=player, cardset=cardset)

    def observe_has(game, player, card):
        game.update_status(player, card, 'has')

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
        possible_cards = [c for c in cardset if
                          not game.definitely_lacks(player, c)]
        if len(possible_cards) == 1:
            game.update_status(player, possible_cards.pop(), 'has')


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
    unlocated_cards = [c for c in game.card_list(card.card_type) if
                       not game.known_to_be_in_a_players_hand(c)]
    if len(unlocated_cards) == 1:
        game.confidential_file.add(unlocated_cards.pop())


@events.on(emitter=em, event='has')
@events.on(emitter=em, event='lacks')
def resolve_hand_size_rule(game, player, card=None):
    cards_having = [c for c in game.cards if game.definitely_has(player, c)]
    cards_lacking = [c for c in game.cards if game.definitely_lacks(player, c)]

    if len(cards_having) == player.hand_size:
        for c in set(game.cards) - set(cards_having):
            game.update_status(player, c, 'lacks')
    elif len(game.cards) - len(cards_lacking) == player.hand_size:
        for c in set(game.cards) - set(cards_lacking):
            game.update_status(player, c, 'has')


@dataclass(frozen=True)
class Card:
    name: str
    card_type: str


@dataclass(frozen=True)
class Player:
    name: str
    hand_size: int
