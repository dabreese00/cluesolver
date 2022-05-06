from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import click
from flask import current_app, g
from flask.cli import with_appcontext

from cluesolver.adapters.orm import mapper_registry
from cluesolver.adapters.repository import SqlAlchemyRepository


def get_db_engine():
    if 'db_engine' not in g:
        g.db_engine = create_engine(current_app.config['DATABASE'])

    return g.db_engine


def get_db():
    engine = get_db_engine()
    if 'db' not in g:
        g.db = Session(engine)

    return g.db


def get_repo():
    db = get_db()
    if 'repo' not in g:
        g.repo = SqlAlchemyRepository(db)

    return g.repo


def close_db(e=None):
    db = g.pop('db', None)
    db_engine = g.pop('db_engine', None)

    if db is not None:
        db.close()

    if db_engine is not None:
        db_engine.dispose()


def close_repo(e=None):
    g.pop('repo', None)
    close_db(e)


def init_db():
    engine = get_db_engine()

    mapper_registry.metadata.drop_all(engine, checkfirst=True)
    mapper_registry.metadata.create_all(engine)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_repo)
    app.cli.add_command(init_db_command)
