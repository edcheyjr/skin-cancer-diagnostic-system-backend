import unittest

from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    # constructor for the user model
    def __init__(self, *args, **kwargs):
        super(TestUserModel, self).__init__(*args, **kwargs)
        self.user_data = User(
            username='test_username',
            email='test@gmail.com',
            password='test_password',
            role="admin",
        )

    def test_encode_auth_token(self):
        user = self.user_data
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        # check if the token is a bytes object
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_auth_token(self):
        user = User(
            username='test_username',
            email='test@gmail.com',
            password='test_password',
            role="admin",
        )
        db.session.add(user)
        db.session.commit()
        # print("user id: ", user.id)
        # print("user public id: ", user.public_id)
        auth_token = user.encode_auth_token(user.id)
        # check if the token is a bytes object
        self.assertTrue(isinstance(auth_token, str))
        # check if the result is a dict
        self.assertTrue(isinstance(User.decode_auth_token(auth_token), dict))
        # assert that the token is valid for the user id 1
        # self.assertTrue(User.decode_auth_token(auth_token).public_id == 1)


if __name__ == '__main__':
    unittest.main()
