import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from cluesolver.adapters.orm import mapper_registry, map_orm
# from cluesolver.config import get_postgres_uri


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    map_orm()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


# @pytest.fixture
# def postgres_db():
#     engine = create_engine(get_postgres_uri())
#     mapper_registry.metadata.create_all(engine)
#     return engine
#
#
# @pytest.fixture
# def postgres_session(postgres_db):
#     map_orm()
#     yield sessionmaker(bind=postgres_db)()
#     clear_mappers()
