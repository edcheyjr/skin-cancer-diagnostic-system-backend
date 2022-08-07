
from app.main.model.user import User
from .blacklist_service import save_token
from flask import jsonify, make_response
from ..config import SUCCESS, FAILURE


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.public_id)
                if auth_token:
                    response_object = {
                        'status': SUCCESS,
                        'message': 'Successfully logged in.',
                        'user': User.serialize(user),
                        'Authorization': auth_token
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': FAILURE,
                    'message': 'email or password does not match.'
                }
                return response_object, 401
        except Exception as e:
            print(e)
            response_object = {
                'status': FAILURE,
                'message': f'Try again,{e}'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if bool(data):
            auth_token = data.split(" ")[1]
            try:
                response = User.decode_auth_token(auth_token)
                if not isinstance(response, str):
                    return save_token(token=auth_token)
                else:
                    return make_response(jsonify({
                        'status': FAILURE,
                        'message': response
                    }), 401)
            except Exception as e:
                response_object = {
                    'status': FAILURE,
                    'message': f'Provide a valid auth token.{e}'
                }
                return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        data = new_request.headers.get('Authorization')
        print("===========================================================")
        print("Content-Type",new_request.headers.get("Content-Type"))
        print("===========================================================")
        print(
            "================================data===============================================")
        print(data)
        print(
            "========================================m============================================")
        if bool(data):
            auth_token = data.split(" ")[1]
            # print(
            #     "=====================================================================================")
            # print(auth_token)
            # print(
            #     "========================================m============================================")
            response = User.decode_auth_token(auth_token)
            # print(
            #     "=====================================================================================")
            # print("response", response)
            # print(
            #     "=====================================================================================")
            if not isinstance(response, str):
                user = User.query.filter_by(
                    public_id=response["public_id"]).first()
                return user, 200
            else:
                response_object = {
                    'status': FAILURE,
                    'message': response
                }
                return response_object, 401
        else:
            return {'status': FAILURE, 'message': 'unauthorized request'}, 403
