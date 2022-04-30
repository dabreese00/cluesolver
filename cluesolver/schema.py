from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)

    players = relationship(
        "Player", back_populates="game", cascade="all, delete-orphan"
    )


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)

    game = relationship("Game", back_populates="players")


class Card(Base):
    __tablename__ = "card"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    card_type = Column(String(30), nullable=False)


def drop_tables(engine):
    Base.metadata.drop_all(engine, checkfirst=True)


def create_tables(engine):
    Base.metadata.create_all(engine)
