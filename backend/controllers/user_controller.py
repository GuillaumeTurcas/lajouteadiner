from flask import Blueprint, jsonify, request
from models.user import *

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["POST"])
def add_user():
    data = request.json
    user = create_user(data["name"], data["surname"], data["login"], data["password"], data["admin"])
    return jsonify(user), 201

@user_bp.route("/users", methods=["GET"])
def list_users():
    users = get_users()
    return jsonify(users), 200

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_id(user_id):
    user = get_user(user_id)
    return jsonify(user), 200

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def modify_user(user_id):
    data = request.json
    user = update_user(user_id, data)
    return jsonify(user), 200

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    delete_user(user_id)
    return jsonify({"message": "User deleted"}), 200
