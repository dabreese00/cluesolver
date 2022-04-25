# Some notes on solving Clue

A *game* involves several cards and several players, and a confidential file.  Every card is either in exactly one player's hand, or in the confidential file.

A *card* is identified by its *name*.  It also has a *type* that's either *person*, *weapon*, or *room*.  I know all cards in the game.

There are several *players*, and each one has a *hand* containing a fixed number of cards (*hand size*).

A *card set* consists of exactly 3 cards, all of different types.

The *confidential file* contains exactly one card set.

A player may *suggest* a card set.

A player may *pass* on a suggested card set, in which case that player has none of the cards in the suggested card set.

A player may *show* on a suggested card set, in which case that player has at least one of the cards in the suggested card set.

The program should gather and deduce information based on observed events and the rules/triggered deductions described.  In particular, we want to deduce the contents of the confidential file.

## Observed events i.e. externally-triggered

- "Observed Pass": We observe that Player Y passes on suggested card set Q.

- "Observed show": We observe that Player X shows on suggested card set Q.

- "Observed has": We observe that Card A is in Player X's hand.

## Deduced facts i.e. triggered by new knowledge gained, internal or external

- "Show-Elimination Rule": If Player Y has shown card set Q, but is known to not have two of the cards in card set Q, then deduce and mark that Player Y has the final card in card set Q.
    - Triggers: Player does not have card OR New Show.
    - Results: Player has card.

- "File-Has-A-Full-Set rule": If we have now marked locations of all but one of the cards of Card A's type, then deduce and mark the location of the final card of this type: The confidential file.
    - Triggers: Player has card.
    - Results: Card is in confidential file.

- "Only-One-Holder Rule": If we know that Card A is in Player X's hand, then deduce and mark that it is not in any other player's hand, or in the confidential file.
    - Triggers: Player has card.
    - Results: Player does not have card.

- "At-Least-One-Holder Rule": If we know that card A is not in any player's hand, then deduce and mark that it's in the one remaining possible location: The confidential file.
    - Triggers: Player does not have card.
    - Results: Card is in confidential file.

- "Hand-Minimum Rule": If we have now marked a number of cards not in Player Y's hand equal to the number of cards in the game minus Player Y's hand size, then deduce and mark the remaining cards in Player Y's hand.
    - Triggers: Player does not have card.
    - Results: Player has card.

- "Hand-Maximum Rule": If we have now marked a number of cards in Player X's hand equal to Player X's hand size, then deduce and mark that all other cards are not in Player X's hand.
    - Triggers: Player has card.
    - Results: Player does not have card.
