from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, registry

import cluesolver.cluegame as cluegame


mapper_registry = registry()


game_table = Table(
    'game',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(30), nullable=False, unique=True),
)


player_table = Table(
    'player',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(30), nullable=False, unique=True),
    Column('game_id', Integer, ForeignKey("game.id"), nullable=False),
    Column('hand_size', Integer),
)


card_table = Table(
    'card',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(30), nullable=False, unique=True),
    Column('game_id', Integer, ForeignKey("game.id"), nullable=False),
    Column('card_type', String(30), nullable=False),
)


def map_orm():
    mapper_registry.map_imperatively(cluegame.Card, card_table)
    mapper_registry.map_imperatively(cluegame.Player, player_table)
    mapper_registry.map_imperatively(
        cluegame.Game, game_table, properties={
            'players': relationship(cluegame.Player,
                                    order_by=player_table.c.id),
            'cards': relationship(cluegame.Card,
                                  order_by=card_table.c.id),
        }
    )
