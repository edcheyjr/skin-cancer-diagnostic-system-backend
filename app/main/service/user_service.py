from datetime import datetime
from app.main import db
from app.main.model.user import User
from ..config import SUCCESS, FAILURE
from ..utils.save_to_db import save_changes


# create a method to create and save a new user


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data['role'],
            date_modified=datetime.now()
        )
        save_changes(new_user)
        return generate_token(new_user), 201
    else:
        response = {
            'status': FAILURE,
            'message': 'User already exists.'
        }
        return response, 409

# create a methode to get all users


def get_all_users():
    return User.query.all()

# create a method to get a user by id


def get_a_user(id):
    return User.query.filter_by(public_id=id).first()

# delete user


def delete_a_user(id):
    user = User.query.filter_by(public_id=id).first_or_404()
    db.session.delete(user)
    return {
        "status": SUCCESS,
        "message": "user deleted"
    }

# generate a token for a user


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.public_id)
        response_object = {
            'status': SUCCESS,
            'message': 'Successfully logged in.',
            'user': User.serialize(user),
            'Authorization': auth_token
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': FAILURE,
            'message': f'Try again,{e}'
        }
        return response_object, 500
