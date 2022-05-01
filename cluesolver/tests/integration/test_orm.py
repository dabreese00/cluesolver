from cluesolver.cluegame import Card


def test_card_mapper_can_load_cards(session):
    session.execute(
        "INSERT INTO card (name, card_type) VALUES (:name, :card_type)",
        [{"name": "Oogal", "card_type": "Person"},
         {"name": "Oogan", "card_type": "Weapon"}, ]
    )
    expected = [
        Card("Oogal", "Person"),
        Card("Oogan", "Weapon"),
    ]
    assert session.query(Card).all() == expected


def test_card_mapper_can_save_cards(session):
    new_card = Card("Oogaz", "Room")
    session.add(new_card)
    session.commit()

    rows = list(session.execute("SELECT name, card_type FROM card"))
    assert rows == [("Oogaz", "Room")]
