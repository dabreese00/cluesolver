# Some notes on solving Clue

A *game* involves several cards and several players, and a confidential file.  Every card is either in exactly one player's hand, or in the confidential file.

A *card* is identified by its *name*.  It also has a *type* that's either *person*, *weapon*, or *room*.  I know all cards in the game.

There are several *players*, and each one has a *hand* containing a fixed number of cards (*hand size*).

A *card set* consists of exactly 3 cards, all of different types.

The *confidential file* contains exactly one card set.

A player may *suggest* a card set.

A player may *pass* on a suggested card set, in which case that player has none of the cards in the suggested card set.

A player may *show* on a suggested card set, in which case that player has at least one of the cards in the suggested card set.


I directly observe the following types of events/raw data:

- Player X exists and has n cards.
- Card A is in Player X's hand.
- [Bonus] Player X suggests card set Q.
- Player Y passes on suggested card set Q.
- Player Z shows on suggested card set Q.

Based on these events and the stated rules, the clue solver application should record all known info about where each card is or is not.  The goal is to identify which card set is in the confidential file.

List of rules and observations used to make deductions:

Observed events:

- "Observed Pass": When we observe that Player Y passes on suggested card set Q, we mark that Card is not in Player Y's hand, for each Card in Card Set Q.
    - Triggers: External.
    - Results: Player does not have card.

- "Observed show you": When we observe that Player X shows on suggested card set Q, we Mark that Card Set Q has been Shown By Player X, Check and mark the Show-Elimination Rule.
    - Triggers: External.
    - Results: Player has shown cardset.

- "Observed show me": Whenever we observe or mark that Card A is in Player X's hand, we mark this, Check and mark the Only-One-Holder rule, Check and mark the Hand-Maximum rule, Check and mark the File-Has-A-Full-Set rule.
    - Triggers: External
    - Results: Player has card.

Deduced/triggered facts:

- "Show-Elimination Rule": If Player Y has shown card set Q, but is known to not have two of the cards in card set Q, then Player Y has the final card in card set Q.
    - Triggers: Player does not have card OR New Show.
    - Results: Player has card.

- "File-Has-A-Full-Set rule": If we have now marked locations of all cards of Card A's type but one, then mark the location of the final one: The confidential file.
    - Triggers: Player has card.
    - Results: Card is in confidential file.

- "Only-One-Holder Rule": If we know that a card is in a player's hand, it cannot be in any other player's hand or in the confidential file.
    - Triggers: Player has card.
    - Results: Player does not have card.

- "At-Least-One-Holder Rule": If we know that card is not in any player's hand, mark it in the one remaining possible location: The confidential file.
    - Triggers: Player does not have card.
    - Results: Card is in confidential file.

- "Hand-Minimum Rule": If we have now marked cards not in Player Y's hand equal to the number of cards in the game minus Player Y's hand size, mark the remaining cards in Player Y's hand.
    - Triggers: Player does not have card.
    - Results: Player has card.

- "Hand-Maximum Rule": If we have now marked cards in Player X's hand equal to Player X's hand size, mark that all other cards are not in Player X's hand.
    - Triggers: Player has card.
    - Results: Player does not have card.


Bonuses/wish list:

- Track and distinguish publicly-known from non-public information.
- Track and make "probable" deductions based on the fact that a player made a certain suggestion (can't glean any definitive info from this).
- Help recommend the best next suggestion to make to gather the most info possible.
