from cluesolver.cluegame import Game

from cluesolver.tests.integration.test_object_views import ObjectViewBase


class TestGamesEndpoint(ObjectViewBase):
    relative_url = '/games'
    post_dict = {'name': 'Oogas'}
    model = Game
    list_key = 'games'
