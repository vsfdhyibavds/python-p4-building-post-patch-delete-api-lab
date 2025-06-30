import json
from os import environ
import re

from flask import request

from server.app import app
from server.models import db, Bakery, BakedGood


import pytest
class TestApp:
    '''Flask application in flask_app.py'''

    def test_creates_baked_goods(self, test_client):
        '''can POST new baked goods through "/baked_goods" route.'''

        with app.app_context():

            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if af:
                db.session.delete(af)
                db.session.commit()

            response = test_client.post(
                '/baked_goods',
                data={
                    "name": "Apple Fritter",
                    "price": 2,
                    "bakery_id": 1,
                }
            )

            af = BakedGood.query.filter_by(name="Apple Fritter").first()

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            assert af.id

    def test_updates_bakeries(self, test_client):
        '''can PATCH bakeries through "bakeries/<int:id>" route.'''

        with app.app_context():

            mb = Bakery.query.filter_by(name="Delightful donuts").first()
            if not mb:
                mb = Bakery(name="Delightful donuts")
                db.session.add(mb)
                db.session.commit()

            mb.name = "ABC Bakery"
            db.session.add(mb)
            db.session.commit()

            response = test_client.patch(
                f'/bakeries/{mb.id}',
                data={
                    "name": "Your Bakery",
                }
            )

            assert response.status_code == 200
            assert response.content_type == 'application/json'

            # Refresh mb from db to get updated name
            db.session.refresh(mb)
            assert mb.name == "Your Bakery"

    def test_deletes_baked_goods(self, test_client):
        '''can DELETE baked goods through "baked_goods/<int:id>" route.'''

        with app.app_context():

            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if not af:
                af = BakedGood(
                    name="Apple Fritter",
                    price=2,
                    bakery_id=5,
                )
                db.session.add(af)
                db.session.commit()

            response = test_client.delete(
                f'/baked_goods/{af.id}'
            )

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert not BakedGood.query.filter_by(name="Apple Fritter").first()
