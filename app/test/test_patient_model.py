import unittest
import json

from app.main import db
from app.test.base import BaseTestCase

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


def add_a_new_patient(self):
    return self.client.post('/patient',
                            data=json.dump(dict(
                                name='john doe',
                                age=21,
                                sex='male',
                                date_created='2019-01-01',
                                date_modified='2019-01-01'
                            )),
                            content_type='application/json',
                            headers=dict(
                                Authorization='Bearer ' + self.get_token()
                            ))


class TestPatientBlueprint(BaseTestCase):
    # test creating a patient
    def test_create_a_new_patient(self):
        """testing a user creating a new patient"""
        with self.client:
            response = register_user(self)
            data = json.loads(response.data)
            response_data = data[0]
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['Authorization'])
            response = add_a_new_patient(self)
            data = json.loads(response.data)
            print("==========================")
            print("data", data)
            print("==========================")
