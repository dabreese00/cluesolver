from dataclasses import dataclass
import event_emitter as events


em = events.EventEmitter()


class Game:
    def __init__(self, cards, players):
        self.cards = cards
        self.players = players
        self.confidential_file = set()

    def card_list(self, card_type):
        return [card for card in self.cards if card.card_type == card_type]

    def observe_pass(self, player, cardset):
        for c in cardset:
            player.lacks(c, self)

    def observe_shown(self, player, cardset):
        player.shows(cardset, self)

    def observe_has(self, player, card):
        player.has(card, self)

    def known_to_be_in_a_players_hand(self, card):
        for p in self.players:
            if card in p.known_cards_held:
                return True
        return False


class Player:
    def __init__(self, name, hand_size=None):
        self.name = name
        self.hand_size = hand_size
        self.known_cards_held = []
        self.known_cards_not_held = []
        self.shown_cardsets = []

    def known_holding_status(self, card):
        if card in self.known_cards_held:
            return "Yes"
        elif card in self.known_cards_not_held:
            return "No"
        else:
            return "Maybe"

    def has(self, card, game):
        if self.known_holding_status(card) == "Maybe":
            self.known_cards_held.append(card)
            em.emit('has', game=game, player=self, card=card)

    def lacks(self, card, game):
        if self.known_holding_status(card) == "Maybe":
            self.known_cards_not_held.append(card)
            em.emit('lacks', game=game, player=self, card=card)

    def shows(self, cardset, game):
        self.shown_cardsets.append(cardset)
        em.emit('shown', game=game, player=self, cardset=cardset)


@events.on(emitter=em, event='shown')
@events.on(emitter=em, event='lacks')
def resolve_show_elimination_rule(game, player, card=None, cardset=None):
    for cardset in player.shown_cardsets:
        possible_cards = [c for c in cardset if
                          c not in player.known_cards_not_held]
        if len(possible_cards) == 1:
            player.has(possible_cards.pop(), game)


@events.on(emitter=em, event='lacks')
def resolve_at_least_one_holder_rule(game, card, player=None):
    for player in game.players:
        if card not in player.known_cards_not_held:
            return
    game.confidential_file.add(card)


@events.on(emitter=em, event='has')
def resolve_at_most_one_holder_rule(game, player, card):
    if card in player.known_cards_held:
        for p in set(game.players) - {player}:
            p.lacks(card, game)


@events.on(emitter=em, event='has')
def resolve_file_has_a_full_set_rule(game, card, player=None):
    unlocated_cards = [c for c in game.card_list(card.card_type) if
                       not game.known_to_be_in_a_players_hand(c)]
    if len(unlocated_cards) == 1:
        game.confidential_file.add(unlocated_cards.pop())


@events.on(emitter=em, event='has')
@events.on(emitter=em, event='lacks')
def resolve_hand_size_rule(game, player, card=None):
    cards_having = [c for c in game.cards if c in player.known_cards_held]
    cards_lacking = [c for c in game.cards if c in player.known_cards_not_held]

    if len(cards_having) == player.hand_size:
        for c in set(game.cards) - set(cards_having):
            player.lacks(c, game)
    elif len(game.cards) - len(cards_lacking) == player.hand_size:
        for c in set(game.cards) - set(cards_lacking):
            player.has(c, game)


@dataclass(frozen=True)
class Card:
    name: str
    card_type: str
