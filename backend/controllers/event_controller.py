from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from models.event import *
from auth import *

# Event namespace
event_ns = Namespace("events", description="Event related operations")

# Event model for Swagger documentation
event_model = event_ns.model("Event", {
    "event": fields.String(required=True, description="Name of the event"),
    "date": fields.DateTime(required=True, dt_format="iso8601", description="Date of the event (YYYY-MM-DD)"),
    "deadline": fields.DateTime(required=True, dt_format="iso8601", description="Deadline to accept (YYYY-MM-DD)"),
    "place": fields.String(required=True, description="Place of the event"),
    "organizer": fields.Integer(required=True, description="Organizer of the event")
})

@event_ns.route("/")
class EventList(Resource):
    @event_ns.doc("list_events")
    @login_required
    @admin_required
    def get(self):
        """List all events"""
        try:
            events = get_events()
            return jsonify(events)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @event_ns.expect(event_model)
    @event_ns.doc("add_event")
    @login_required
    def post(self):
        """Create a new event"""
        try:
            verify_jwt_in_request()  # Vérifie que le JWT est valide
            current_user = json.loads(get_jwt_identity())
            data = request.json
            if "organizer" in data:
                if current_user["user_id"] != data["organizer"] and current_user["admin"] < 1:
                    return {"error": "You don't have the permission"}
            event = create_event(data["event"], data["date"], data["deadline"], data["place"], data["organizer"])
            return jsonify(event)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@event_ns.route("/<int:event_id>")
@event_ns.param("event_id", "The event identifier")
class Event(Resource):
    @event_ns.expect(event_model)
    @event_ns.doc("modify_event")
    @login_required
    @admin_or_organizer_required
    def put(self, event_id):
        """Update an event by ID"""
        try:
            data = request.json
            event = update_event(event_id, data)
            return jsonify(event)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @event_ns.doc("remove_event")
    @login_required
    @admin_or_organizer_required
    def delete(self, event_id):
        """Delete an event by ID"""
        try:
            delete_event(event_id)
            return jsonify({"message": "Event deleted"})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @event_ns.doc("list_event_by_id")
    @login_required
    @admin_or_guests_required
    def get(self, event_id):
        """List an event with his id"""
        try:
            events = get_event(event_id)
            return jsonify(events)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@event_ns.route("/guests/<int:event_id>")
@event_ns.param("event_id", "The event identifier")
class GuestsEvent(Resource):
    @event_ns.doc("list_guest_event")
    @login_required
    @admin_or_guests_required
    def get(self, event_id):
        """List all guest for an event"""
        try:
            events = get_detailed_guests_event(event_id)
            return jsonify(events)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@event_ns.route("/upcoming/<int:user_id>")
@event_ns.param("user_id", "The user identifier")
class UpcomingUserEvents(Resource):
    @event_ns.doc("list_upcoming_user_events")
    @login_required
    @admin_or_owner_required
    def get(self, user_id):
        """List upcoming events for a specific user"""
        try:
            events = get_upcoming_events_user(user_id)
            return jsonify(events)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@event_ns.route("/upcoming")
class UpcomingEvents(Resource):
    @event_ns.doc("list_upcoming_events")
    @login_required
    @admin_required
    def get(self):
        """List all upcoming events"""
        try:
            events = get_upcoming_events()
            return jsonify(events)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@event_ns.route("/user/<int:user_id>")
@event_ns.param("user_id", "The user identifier")
class UserEvents(Resource):
    @event_ns.doc("list_user_events")
    @login_required
    @admin_or_owner_required
    def get(self, user_id):
        """List all events for a specific user"""
        try:
            events = get_events_user(user_id)
            return jsonify(events)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})
