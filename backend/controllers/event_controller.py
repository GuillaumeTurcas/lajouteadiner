from flask import Blueprint, jsonify, request
from models.event import *

event_bp = Blueprint("event", __name__)

#CRUD

@event_bp.route("/events", methods=["POST"])
def add_event():
    data = request.json
    event = create_event(data["event"], data["date"], data["place"], data["organizer"])
    return jsonify(event), 201

@event_bp.route("/events", methods=["GET"])
def list_events():
    events = get_events()
    return jsonify(events), 200

@event_bp.route("/events/<int:event_id>", methods=["PUT"])
def modify_event(event_id):
    data = request.json
    event = update_event(event_id, data)
    return jsonify(event), 200

@event_bp.route("/events/<int:event_id>", methods=["DELETE"])
def remove_event(event_id):
    delete_event(event_id)
    return jsonify({"message": "Event deleted"}), 200

@event_bp.route("/upcoming_events/<int:user_id>", methods=["GET"])
def list_upcoming_user_events(user_id):
    events = get_user_upcoming_events(user_id)
    return jsonify(events), 200

@event_bp.route("/upcoming_events", methods=["GET"])
def list_upcoming_events(user_id):
    events = get_upcoming_events()
    return jsonify(events), 200

@event_bp.route("/events_user/<int:user_id>", methods=["GET"])
def list_user_events(user_id):
    events = get_user_events(user_id)
    return jsonify(events), 200
