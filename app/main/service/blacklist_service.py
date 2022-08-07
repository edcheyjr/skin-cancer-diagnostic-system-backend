from app.main import db
from app.main.model.blacklist import Blacklisted
from ..config import SUCCESS, FAILURE


def save_token(token):
    blacklist_token = Blacklisted(token=token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': SUCCESS,
            'message': 'Token blacklisted.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': FAILURE,
            'message': e
        }
        return response_object, 409
