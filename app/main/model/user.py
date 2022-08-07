from .. import db
import uuid
import datetime
import jwt
from ..config import key
from .blacklist import Blacklisted
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import jsonify


# create a class for the user
class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime)

    # create a constructor for the user model
    def __init__(self, username, email, password, role, date_modified):
        self.username = username
        self.email = email
        self.role = role
        self.public_id = str(uuid.uuid4())
        self.password = password
        self.date_modified = date_modified

    # create a method to serialize the user model

    def serialize(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'date_created':  datetime.datetime.strftime(self.date_created, "%d/%m/%Y, %H:%M:%S"),
            'date_modified':  datetime.datetime.strftime(self.date_modified, "%d/%m/%Y, %H:%M:%S")
        }

    # create a method to deserialize the user model
    def deserialize(self, data):
        self.id = data['id']
        self.public_id = data['public_id']
        self.username = data['username']
        self.email = data['email']
        self.role = data['role']
        self.date_created = data['date_created']
        self.date_modified = data['date_modified']

    # password property

    @property
    def password(self):
        raise AttributeError('password: is a write-only attribute')

    # create a method to set the password
    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string

        """
        try:
            is_blacklisted_token = Blacklisted.is_token_blacklisted(auth_token)
            print(
                "+===========================================================================+")
            print("Ispresent in blacklist table", is_blacklisted_token)
            print(
                "+===========================================================================+")
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                payload = jwt.decode(auth_token, key, algorithms='HS256')
                return {"public_id": payload['sub']}
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User %r>' % self.email  # return the user's email
