import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from app.main.config import basedir

'''
   This classes tests the configuration of the application.
   The test cases are based on the following:
   1. The test_config.py file
   2. The config.py file
   3. The app.py file
   4. The main.py file
   5. The model.py file
   6. The user.py file
   7. The database.py file
   8. The database.sqlite file
   9. The database.sqlalchemy file

'''


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv(
                'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flask_main.db'))
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv(
                'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flask_main.db'))
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.ProductionConfig')
        return app

    # confirm the database is set to the production database and confirm the secret key is not the default
    def test_app_is_production(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(app.config['DEBUG'])
