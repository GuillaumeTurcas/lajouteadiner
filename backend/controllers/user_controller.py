from flask import jsonify, request, session
from flask_restx import Namespace, Resource, fields
from models.user import (
    get_users, create_user, get_user, get_full_user, login_user,
    update_user, delete_user, change_password, reset_password
)
from auth import *

# Initialisation du namespace RESTX
user_ns = Namespace("users", description="User related operations")

# ----------------------------
# Modèles Flask-RESTX pour Swagger
# ----------------------------
user_model = user_ns.model("User", {
    "name": fields.String(required=True, description="First name of the user"),
    "surname": fields.String(required=True, description="Last name of the user"),
    "login": fields.String(required=True, description="Login identifier of the user"),
    "password": fields.String(required=True, description="Password of the user"),
    "admin": fields.Integer(required=True, description="Whether the user is an admin")
})

edit_user_model = user_ns.model("EditUser", {
    "name": fields.String(required=True, description="First name of the user"),
    "surname": fields.String(required=True, description="Last name of the user"),
    "login": fields.String(required=True, description="Login identifier of the user"),
    "admin": fields.Integer(required=True, description="Whether the user is an admin")
})

login_model = user_ns.model("Login", {
    "login": fields.String(required=True, description="Login identifier of the user"),
    "password": fields.String(required=True, description="Password of the user")
})

password_model = user_ns.model("ChangePassword", {
    "old_password": fields.String(required=True, description="Old password of the user"),
    "new_password": fields.String(required=True, description="New password of the user")
})

# ----------------------------
# Routes pour les utilisateurs
# ----------------------------
@user_ns.route("/")
class UserList(Resource):
    @user_ns.doc("list_users")
    @login_required
    @admin_required
    def get(self):
        """List all users."""
        users = get_users()
        return jsonify(users)

    @user_ns.expect(user_model)
    @user_ns.doc("add_user")
    def post(self):
        """Create a new user."""
        data = request.json
        admin = 0
        print(admin)
        if "admin" in session:
            if data["admin"] <= session["admin"]:
                admin = data["admin"]
        user = create_user(
            data["name"], data["surname"],
            data["login"], data["password"], admin
        )
        return jsonify(user)


@user_ns.route("/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class User(Resource):
    @user_ns.doc("get_user")
    @login_required
    def get(self, user_id):
        """Get a user by ID."""
        user = get_user(user_id)
        return jsonify(user)

    @user_ns.expect(edit_user_model)
    @user_ns.doc("modify_user")
    @login_required
    @admin_or_owner_required
    def put(self, user_id):
        """Update a user by ID."""
        data = request.json
        if "admin" in data:
            if data["admin"] > session["admin"]:
                return {"error": "No authorization to make an admin"}
        control_list = ["salt", "token", "password", "id"]
        for control in control_list:
            if control in data:
                if session["admin"] != 2:
                    return {"error": f"No authorization to change {control}"}
        user = update_user(user_id, data)
        return jsonify(user)

    @user_ns.doc("remove_user")
    @login_required
    @admin_or_owner_required
    def delete(self, user_id):
        """Delete a user by ID."""
        delete_user(user_id)
        return jsonify({"message": "User deleted"})


@user_ns.route("/full/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class FullUser(Resource):
    @login_required
    @admin_or_owner_required
    @user_ns.doc("get_full_user")
    def get(self, user_id):
        """Get full details of a user."""
        user = get_full_user(user_id)
        return jsonify(user)


# ----------------------------
# Authentification
# ----------------------------
@user_ns.route("/login")
class Login(Resource):
    @user_ns.expect(login_model)
    @user_ns.doc("login_user")
    def post(self):
        """Login a user."""
        data = request.json
        user = login_user(data["login"], data["password"])
        if user is not None:
            print(f"{user["surname"]} {user["name"]} est connecté")
            session["logged_in"] = True
            session["user"] = user["id"]
            session["login"] = user["login"]
            session["admin"] = user["admin"]
            session["token"] = user["token"]
        return jsonify(user)


@user_ns.route("/change_password/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class ChangePassword(Resource):
    @user_ns.expect(password_model)
    @user_ns.doc("change_password")
    @login_required
    @admin_or_owner_required
    def put(self, user_id):
        """Change a user"s password."""
        data = request.json
        response = change_password(user_id, data["old_password"], data["new_password"])
        return jsonify({"change_password": response})


@user_ns.route("/reset_password/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class ResetPassword(Resource):
    @user_ns.doc("reset_password")
    @login_required
    @admin_or_owner_required
    def post(self, user_id):
        """Reset a user"s password."""
        response = reset_password(user_id)
        return jsonify({"change_password": response})

@user_ns.route("/logout")
class Logout(Resource):
    @user_ns.doc("logout_user")
    def post(self):
        """Logout a user."""
        if session["logged_in"]:
            session.pop("user", None)
            session.pop("admin", None)
            session.pop("login", None)
            session.pop("token", None)
        session["logged_in"] = False
        return jsonify({"logout": True})
