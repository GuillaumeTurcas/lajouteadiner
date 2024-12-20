from flask import jsonify, request, make_response
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (JWTManager, create_access_token, 
    create_refresh_token, jwt_required, get_jwt_identity, get_csrf_token, verify_jwt_in_request)
from models.user import (
    get_users, create_user, get_user, get_full_user, login_user,
    update_user, delete_user, change_password, reset_password
)
from auth import *
from datetime import datetime, timedelta
import pytz
from json import dumps
from config import limit_session, BLOCKLIST

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
    def get(self):
        """List all users."""
        try:
            users = get_users()
            return jsonify(users)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @user_ns.expect(user_model)####################
    @user_ns.doc("add_user")
    def post(self):
        """Create a new user."""
        try:
            data = request.json
            admin = 0
            # Vérifie que le JWT est valide
            verify_jwt_in_request()
            current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT

            if current_user:
                current_user = json.loads(get_jwt_identity())
                if "admin" in data:
                    if data["admin"] > current_user["admin"]:
                        return {"error": "No authorization to make an admin"}
                if "admin" in current_user:
                    if data["admin"] <= current_user["admin"]:
                        admin = data["admin"]
            print(data)
            user = create_user(
                data["name"], data["surname"],
                data["login"], data["password"], admin
            )
            return jsonify(user)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})


@user_ns.route("/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class User(Resource):
    @user_ns.doc("get_user")
    @login_required
    def get(self, user_id):
        """Get a user by ID."""
        try:
            user = get_user(user_id)
            return jsonify(user)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @user_ns.expect(edit_user_model)##############
    @user_ns.doc("modify_user")
    @login_required
    @admin_or_owner_required
    @jwt_required()
    def put(self, user_id):
        """Update a user by ID."""
        try:
            data = request.json
            verify_jwt_in_request()  # Vérifie que le JWT est valide
            current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT

            if current_user:
                current_user = json.loads(get_jwt_identity())
                if "admin" in data:
                    if data["admin"] > current_user["admin"]:
                        return {"error": "No authorization to make an admin"}
            control_list = ["salt", "token", "password", "id"]
            for control in control_list:
                if control in data:
                    if current_user["admin"] != 2:
                        return {"error": f"No authorization to change {control}"}
            user = update_user(user_id, data)
            return jsonify(user)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @user_ns.doc("remove_user")
    @login_required
    @admin_or_owner_required
    def delete(self, user_id):
        """Delete a user by ID."""
        try:
            delete_user(user_id)
            return jsonify({"message": "User deleted"})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})


@user_ns.route("/full/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class FullUser(Resource):
    @login_required
    @admin_or_owner_required
    @user_ns.doc("get_full_user")
    def get(self, user_id):
        """Get full details of a user."""
        try:
            user = get_full_user(user_id)
            return jsonify(user)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})


# ----------------------------
# Authentification
# ----------------------------
@user_ns.route("/login")
class Login(Resource):
    @user_ns.expect(login_model)
    @user_ns.doc("login_user")
    def post(self):
        """Login a user and set JWT in cookies."""
        try:
            data = request.json
            user = login_user(data["login"], data["password"])
            if user is not None:
                expires = timedelta(hours=limit_session)
                access_token = create_access_token(
                    identity=dumps({
                        "user_id": user["id"],
                        "logged_in": True,
                        "name": user["name"],
                        "surname": user["surname"],
                        "login": user["login"],
                        "admin": user["admin"]
                    }),
                    expires_delta=expires
                )
                response = make_response(jsonify({"message": "Logged in successfully"}))
                response.set_cookie("access_token_cookie", access_token)
                return response
            else:
                return jsonify({"msg": "Invalid credentials"})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})


@user_ns.route("/change_password/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class ChangePassword(Resource):
    @user_ns.expect(password_model)
    @user_ns.doc("change_password")
    @login_required
    @admin_or_owner_required
    def put(self, user_id):
        """Change a user"s password."""
        try:
            data = request.json
            response = change_password(user_id, data["old_password"], data["new_password"])
            return jsonify({"change_password": response})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})
            

@user_ns.route("/reset_password/<int:user_id>")
@user_ns.param("user_id", "The user identifier")
class ResetPassword(Resource):
    @user_ns.doc("reset_password")
    @login_required
    @admin_or_owner_required
    def post(self, user_id):
        """Reset a user"s password."""
        try:
            response = reset_password(user_id)
            return jsonify({"change_password": response})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@user_ns.route("/logout")
class Logout(Resource):
    @user_ns.doc("logout_user")
    def post(self):
        """Logout a user by invalidating the JWT and optionally removing the cookie."""
        try:
            # Générer un nouveau token avec logged_in=False
            new_token = create_access_token(
                identity=dumps({  # Sérialiser en JSON
                    "logged_in": False
                })
            )

            # Créer une réponse et ajouter le JWT dans un cookie
            response = make_response(jsonify({"message": "Logged out successfully"}))
            response.set_cookie("access_token_cookie", new_token, httponly=True)
            response.set_cookie("csrf_access_token", "") 

            return response

        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@user_ns.route("/is_login")
class Is_login(Resource):    
    @user_ns.doc("is_login")
    @login_required
    def get(self):
        """Return True if user is login."""
        try:
            return jsonify({
                "is_login": True
                })
        except Exception as e:
            return jsonify({
                "is_login": False
                })
