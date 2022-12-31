# from cluesolver.adapters.repository import AbstractRepository
# import cluesolver.service_layer.services as services
#
#
# class FakeRepository(AbstractRepository):
#     def __init__(self, games):
#         self._games = set(games)
#
#     def add(self, game):
#         self._games.add(game)
#
#     def get(self, name):
#         return next(g for g in self._games if g.name == name)
#
#     def list(self):
#         return list(self._games)
#
#
# class FakeSession:
#     committed = False
#
#     def commit(self):
#         self.committed = True
#
#
# def test_add_game():
#     repo, session = FakeRepository([]), FakeSession()
#     services.add_game("g1", repo, session)
#     assert repo.get("g1") is not None
#     assert session.committed
#
#
# def test_add_card():
#     repo, session = FakeRepository([]), FakeSession()
#     services.add_game("g1", repo, session)
#     services.add_card("c1", "Room", "g1", repo, session)
#     assert "c1" in [c.name for c in repo.get("g1").cards]
#     assert session.committed
#
#
# def test_add_player():
#     repo, session = FakeRepository([]), FakeSession()
#     services.add_game("g1", repo, session)
#     # TODO: Why does this assertion fail???
#     # assert "c1" not in [c.name for c in repo.get("g2").cards]
#     services.add_player("p1", 3, "g1", repo, session)
#     assert "p1" in [p.name for p in repo.get("g1").players]
#     assert session.committed
