#!/usr/bin/env python3

import pytest
from flask_migrate import upgrade
from alembic.config import Config
from server.app import app, db
import server.seed as seed

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        # Run migrations
        config = Config("server/alembic.ini")
        upgrade(config=config)

        # Seed the database
        seed.main()

        testing_client = app.test_client()
        yield testing_client

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
