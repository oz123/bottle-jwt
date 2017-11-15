# -*- coding: utf-8 -*-
"""Example usage.
"""

from __future__ import unicode_literals
import bottle
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required,
                        JWTForbiddenError)


app = bottle.Bottle()

server_secret = '*Y*^%JHg7623'


class AuthBackend(object):
    """Implementing an auth backend class with at least two methods.
    """
    users = {'pav': {'id': 1237832, 'username': 'pav', 'password': '123',
                     'data': {'sex': 'male', 'active': True,
                              'role': 'user'}},
             'admin': {'id': 1237834, 'username': 'pav', 'password': '123',
                       'data': {'sex': 'female', 'active': True,
                                'role': 'manager'}}
             }

    def authenticate_user(self, username, password):
        """Authenticate User by username and password.

        Returns:
            A dict representing User Record or None.
        """
        if username in AuthBackend.users:
            user = AuthBackend.users[username]
            if password == user['password']:
                return user

        return None

    def get_user(self, user_id):
        """Retrieve User By ID.

        Returns:
            A dict representing User Record or None.
        """
        if user_id in AuthBackend.users:
            user = AuthBackend.users[user_id]
            user_no_pass = user.copy()
            user_no_pass.pop('password')
            return user_no_pass
        return None


provider_plugin = JWTProviderPlugin(
    keyword='jwt',
    auth_endpoint='/auth',
    backend=AuthBackend(),
    fields=('username', 'password'),
    secret=server_secret,
    ttl=3000,
    **{'id_field': 'username'}

)


app.install(provider_plugin)


def do_check_here(role):
    user = bottle.request.get_user()
    if user['data']['role'] != role:
        raise JWTForbiddenError("Can't access this resource!")


def auth_require(role=None):
    def decorator(func):
        def wrapper(*a, **ka):
            do_check_here(role)
            return func(*a, **ka)
        return wrapper
    return decorator


@app.get('/admin')
@jwt_auth_required
@auth_require(role="admin")
def admin_resource():
    return {"admin": "admin area!", "user": bottle.request.get_user()}


@app.get('/')
@jwt_auth_required
@auth_require(role="user")
def private_resource():
    return {"scope": "For your eyes only!", "user": bottle.request.get_user()}


bottle.debug(True)
bottle.run(
    app=app, port=9092, host='0.0.0.0', reloader=True)
