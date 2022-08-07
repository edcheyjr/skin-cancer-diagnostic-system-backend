import unittest
import json
from app.test.base import BaseTestCase
from app.main import db
from app.main.model.blacklist import Blacklisted

# register a new user


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            username='john doe',
            email='john@gmail.com',
            password='12345678',
            role='doc',
            date_created='2019-01-01',
            date_modified='2019-01-01'
        )),
        content_type='application/json',
        # headers=dict(
        #     Authorization='Bearer ' + self.get_token()
        # )
    )

# login a user


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='john@gmail.com',
            password='12345678'
        )),
        content_type='application/json'
    )

# test auth blueprint


class TestAuthBlueprint(BaseTestCase):
    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'fail')
            # self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_registration(self):
        """ Test for login of registered-user login """

        response = register_user(self)
        data = json.loads(response.data)
        status = data[1]
        response_data = data[0]
        self.assertTrue(response_data['Authorization'])
        self.assertTrue(response_data['status'] == 'success')
        #self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(status, 200)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        register_user(self)
        with self.client:
            response = register_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'fail')
            #self.assertTrue(data['message'] == 'User already exists. Please Log in.')
            self.assertEqual(response.status_code, 409)

    def test_registered_user_login(self):
        """ Test for login of registered user"""
        with self.client:
            # user registration
            response = register_user(self)
            data = json.loads(response.data)
            status = data[1]
            response_data = data[0]

            self.assertTrue(response_data['status'] == 'success')
            #self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(status, 200)
            # user login
            response = login_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'success')
            #self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            response = register_user(self)
            data = json.loads(response.data)
            response_data = data[0]
            self.assertTrue(response_data['status'] == 'success')
            #self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # user login
            response = login_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'success')
            #self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(response.data)['Authorization']
                )
            )
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'success')
            #self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a token expires """
        with self.client:
            # user registration
            response = register_user(self)
            data = json.loads(response.data)
            response_data = data[0]
            self.assertTrue(response_data['status'] == 'success')
            #self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # user login
            response = login_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'success')
            #self.assertTrue(data['message'] == 'Successfully logged in.') # noqa: E501
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # blacklist a valid token
            blacklist_token = Blacklisted(
                token=json.loads(response.data)['Authorization'])
            db.session.add(blacklist_token)
            db.session.commit()

            # blacklisted valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' +
                    json.loads(response.data)['Authorization']
                )
            )
            data = json.loads(response.data)
            self.assertTrue(data['status'] == 'fail')
            #self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
