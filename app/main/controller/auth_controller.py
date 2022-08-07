from email import header
from flask import request
from flask_restx import Resource

from ..utils.dto import AuthDto
from ..service.auth_helper import Auth
from ..utils.decorator import token_required

# create a namespace
api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    # @api.header("Access-Control-Allow-Origin", "http://localhost:3000/")
    def post(self):
        post_data = request.json
        return Auth.login_user(post_data)


@api.route('/logout')
class UserLogout(Resource):
    """
    Logout a user Resource
    """
    @token_required
    @api.doc('logout a user')
    def post(self):
        # get the post data
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
