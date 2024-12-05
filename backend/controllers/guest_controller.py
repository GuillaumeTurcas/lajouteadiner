from flask import Blueprint, jsonify, request
from models.guest import create_guest, get_guests, update_guest, delete_guest

guest_bp = Blueprint("guest", __name__)

@guest_bp.route("/guests", methods=["POST"])
def add_guest():
    data = request.json
    guest = create_guest(data["user"], data["event"], data["role"])
    return jsonify(guest), 201

@guest_bp.route("/guests", methods=["GET"])
def list_guests():
    guests = get_guests()
    return jsonify(guests), 200

@guest_bp.route("/guests/<int:guest_id>", methods=["PUT"])
def modify_guest(guest_id):
    data = request.json
    guest = update_guest(guest_id, data)
    return jsonify(guest), 200

@guest_bp.route("/guests/<int:guest_id>", methods=["DELETE"])
def remove_guest(guest_id):
    delete_guest(guest_id)
    return jsonify({"message": "Guest deleted"}), 200

