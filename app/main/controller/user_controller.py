from flask import jsonify, make_response, request
from flask_restx import Resource
from sqlalchemy import null

from ..utils.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user
from ..utils.decorator import admin_token_required

# create a namespace for the user controller
api = UserDto.api
_user = UserDto.user
_user_register = UserDto.user_register

# user controller


@api.route('/')
class UserList(Resource):

    @admin_token_required
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    # post a new user
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')  # add a description to the post method
    # add a validation to the post method
    @api.expect(_user_register, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data)

# user controller by id


@api.route('/<public_id>')
class User(Resource):
    @admin_token_required
    @api.doc('get a user by id')
    @api.marshal_with(_user)
    # auth decorator for protected endpoints (i.e. endpoints that require a valid admin token)
    def get(self, public_id):
        """get a user given its id"""
        user = get_a_user(public_id)
        if user.public_id == null:
            make_response({"error", "unauthorized request"}, 401)
        else:
            if not user:
                api.abort(404, "User not found")
            return user  #
