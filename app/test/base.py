from flask_testing import TestCase
from app.main import db
from manage import app

class BaseTestCase(TestCase):
  ''' base case testing '''

  @classmethod
  def create_app(self):
    ''' create app '''
    app.config.from_object('app.main.config.TestingConfig')
    return app

  @classmethod
  def setUp (self):
    ''' set up '''
    db.create_all()
    db.session.commit()

  @classmethod
  def tearDown(self):
    ''' tear down '''
    db.session.remove()
    db.drop_all()
