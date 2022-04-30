# from ...cluegame import Game


# def test_player_mapper_can_load_players(session):
#     session.execute(
#         "INSERT INTO games (name) VALUES ?",
#         [("Oogal",), ("Oogan",), ]
#     )
#     expected = [
#         Game("Oogal"),
#         Game("Oogan"),
#     ]
#     assert session.query(Game).all() == expected
