from flask import Blueprint, jsonify, request
from models.assign import create_assign, get_assigns, update_assign, delete_assign

assign_bp = Blueprint("assign", __name__)

@assign_bp.route("/assigns", methods=["POST"])
def add_assign():
    data = request.json
    assign = create_assign(data["user"], data["item"], data["quantity"])
    return jsonify(assign), 201

@assign_bp.route("/assigns", methods=["GET"])
def list_assigns():
    assigns = get_assigns()
    return jsonify(assigns), 200

@assign_bp.route("/assigns/<int:assign_id>", methods=["PUT"])
def modify_assign(assign_id):
    data = request.json
    assign = update_assign(assign_id, data)
    return jsonify(assign), 200

@assign_bp.route("/assigns/<int:assign_id>", methods=["DELETE"])
def remove_assign(assign_id):
    delete_assign(assign_id)
    return jsonify({"message": "Assign deleted"}), 200
