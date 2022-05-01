import pytest
from sqlalchemy import select

from cluesolver.cluegame import Player
from cluesolver.db import get_db

from cluesolver.tests.integration.test_object_views import ObjectViewBase


class TestPlayerViews(ObjectViewBase):
    relative_url = '/players'
    post_dict = {
        'name': 'Benji',
        'game_id': 1,
        'hand_size': 3,
    }
    model = Player
    list_key = 'players'

    def test_list(self):
        pass

    def test_get(self):
        pass

    def test_get_nonexistent_returns_404(self):
        pass
