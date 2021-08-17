from typing import Dict, Tuple

from app.main.service.auth_helper import Auth
from app.main.util.decorator import admin_token_required
from flask import request
from flask_restx import Resource

from ..service.user_service import (get_a_user, get_all_users, get_user_delete,
                                    save_new_user)
from ..util.dto import UserDto

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.doc('remove user')
    @api.marshal_with(_user)
    def post(self, public_id):
        """get a user given their identifier and remove"""
        user = get_user_delete(public_id)
        auth_header = request.headers.get('Authorization')
        Auth.logout_user(data=auth_header)
        return user



