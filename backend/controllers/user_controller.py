from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from models.user import *

user_ns = Namespace('users', description='User related operations')

# User model for Swagger documentation
user_model = user_ns.model('User', {
    'name': fields.String(required=True, description='First name of the user'),
    'surname': fields.String(required=True, description='Last name of the user'),
    'login': fields.String(required=True, description='Login identifier of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'admin': fields.Integer(required=True, description='Whether the user is an admin')
})

edit_user_model = user_ns.model('User', {
    'name': fields.String(required=True, description='First name of the user'),
    'surname': fields.String(required=True, description='Last name of the user'),
    'login': fields.String(required=True, description='Login identifier of the user'),
    'admin': fields.Integer(required=True, description='Whether the user is an admin')
})


login_model = user_ns.model('Login', {
    'login': fields.String(required=True, description='Login identifier of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

password_model = user_ns.model('ChangePassword', {
    'old_password': fields.String(required=True, description='Old password of the user'),
    'new_password': fields.String(required=True, description='New password of the user')
})

@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('list_users')
    def get(self):
        """List all users"""
        users = get_users()
        return jsonify(users)

    @user_ns.expect(user_model)
    @user_ns.doc('add_user')
    def post(self):
        """Create a new user"""
        data = request.json
        user = create_user(data['name'], data['surname'], data['login'], data['password'], data['admin'])
        return jsonify(user)

@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'The user identifier')
class User(Resource):
    @user_ns.doc('get_user')
    def get(self, user_id):
        """Get a user by ID"""
        user = get_user(user_id)
        return jsonify(user)

    @user_ns.expect(edit_user_model)
    @user_ns.doc('modify_user')
    def put(self, user_id):
        """Update a user by ID"""
        data = request.json
        user = update_user(user_id, data)
        return jsonify(user)

    @user_ns.doc('remove_user')
    def delete(self, user_id):
        """Delete a user by ID"""
        delete_user(user_id)
        return jsonify({'message': 'User deleted'})


### Login ###

@user_ns.route("/login")
class login(Resource):
    @user_ns.expect(login_model)
    @user_ns.doc('login_user')
    def post(self):
        data = request.json
        user = login_user(data["login"], data["password"])
        if user != None:
            print(f"{user["surname"]} {user["name"]} est connecté")
        return jsonify(user)

@user_ns.route("/change_password/<int:user_id>")
class password(Resource):
    @user_ns.expect(password_model)
    @user_ns.doc('change_password')
    def put(self, user_id):
        data = request.json
        response = change_password(user_id, data["old_password"], data["new_password"])
        return jsonify({"change_password": response})

@user_ns.route("/reset_password/<int:user_id>")
class password(Resource):
    @user_ns.doc('reset_password')
    def post(self, user_id):
        response = reset_password(user_id)
        return jsonify({"change_password": response})