# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user
from flask_restful import Api, Resource

from ..user import User


api = Blueprint('api', __name__, url_prefix='/api')
api_wrap = Api(api)


class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

api_wrap.add_resource(TodoItem, '/todos/<int:id>')


@api.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated():
        return jsonify(flag='success')

    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        user, authenticated = User.authenticate(username, password)
        if user and authenticated:
            if login_user(user, remember='y'):
                return jsonify(flag='success')

    return jsonify(flag='fail', msg='Sorry, try again.')


@api.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
    return jsonify(flag='success', msg='Logouted.')
