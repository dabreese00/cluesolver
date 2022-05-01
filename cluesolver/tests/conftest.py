import os
import tempfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from cluesolver import create_app
from cluesolver.db import init_db
from cluesolver.orm import mapper_registry, map_orm


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': 'sqlite:///' + db_path,
    })

    with app.app_context():
        init_db()
        map_orm()

    yield app

    clear_mappers()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.drop_all(engine, checkfirst=True)
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    map_orm()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
