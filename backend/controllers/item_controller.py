from flask import Blueprint, jsonify, request
from models.item import *
import json

item_bp = Blueprint("item", __name__)

@item_bp.route("/items", methods=["POST"])
def add_item():
    data = request.json
    item = create_item(data["name"], data["quantity"], data["description"], data["event"])
    return jsonify(item), 201

@item_bp.route("/items", methods=["GET"])
def list_items():
    items = get_items()
    return jsonify(items), 200

@item_bp.route("/items/<int:item_id>", methods=["PUT"])
def modify_item(item_id):
    data = request.json
    item = update_item(item_id, data)
    return jsonify(item), 200

@item_bp.route("/items/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    delete_item(item_id)
    return jsonify({"message": "Item deleted"}), 200

@item_bp.route("/items_event/<int: event_id>", methods=["GET"])
def items_user(event_id):
 
    items = get_items_event("event_id")
    return jsonify(json.dumps(items)), 200

