import abc

import cluesolver.domain.cluegame as cluegame


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, game: cluegame.Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, name):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, game: cluegame.Game):
        return self.session.add(game)

    def get(self, name):
        return (self.session.query(cluegame.Game).
                filter_by(name=name).one())

    def list(self):
        return list(self.session.query(cluegame.Game).all())
