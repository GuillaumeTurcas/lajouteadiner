from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (JWTManager, create_access_token, 
    create_refresh_token, jwt_required, get_jwt_identity, 
    get_csrf_token, verify_jwt_in_request)
from models.guest import *
from auth import *
from datetime import datetime
import pytz

# Guest namespace
guest_ns = Namespace("guests", description="Guest related operations")

# Guest model for Swagger documentation
guest_model = guest_ns.model("Guest", {
    "user": fields.Integer(required=True, description="User ID of the guest"),
    "event": fields.Integer(required=True, description="Event ID the guest is assigned to")
})

guest_accept_model = guest_ns.model("Accept", {
    "accept": fields.Boolean(required=True, description="If the user want to go to the event or not")
})

@guest_ns.route("/")
class GuestList(Resource):
    @guest_ns.doc("list_guests")
    @login_required
    @admin_required
    def get(self):
        """List all guests"""
        try:
            guests = get_guests()
            return jsonify(guests)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @guest_ns.expect(guest_model)
    @guest_ns.doc("add_guest")
    @login_required
    def post(self):
        """Create a new guest"""
        try:
            data = request.json
            verify_jwt_in_request()  
            current_user = json.loads(get_jwt_identity())
            if "event" in data:
                if get_event(data["event"]) \
                    .get("organizer") == current_user["user_id"] \
                    or current_user["admin"] >= 1:
                    guest = create_guest(data["user"], data["event"]) \
                        if authorize(data) \
                        else None
                else:
                    return jsonify({"error": "You are not the organizer or an admin to add a guest"})
            return jsonify(guest)
        except:
            return jsonify({"error": "Impossible to create a new guest"})

@guest_ns.route("/<int:guest_id>") 
@guest_ns.param("guest_id", "The guest identifier") 
class Guest(Resource):
    @guest_ns.doc("get_guest")
    @login_required
    @admin_or_guests_required
    def get(self, guest_id):
        """Get a guest by ID"""
        try:
            guest = get_guest(guest_id)
            return jsonify(guest)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})


    @guest_ns.expect(guest_accept_model)
    @guest_ns.doc("accept_guest")
    @login_required
    @admin_or_guest_required
    def put(self, guest_id):
        """A guest change his decision to go to an event"""
        try:
            data = request.json
            guest_prov = get_guest(guest_id)
            event_prov = get_event(guest_prov["event"])
            if guest_prov["user"] == event_prov["organizer"]:
                return jsonify({"error": "The organizer can't change his decision"})
            if event_prov["deadline"]:
                deadline = datetime.fromisoformat(event_prov["deadline"])
                now_utc = datetime.now(pytz.utc)
                if now_utc > deadline:
                    return jsonify({
                        "too_late": True
                        })
            guest = accept_guest(guest_id, data)
            return jsonify({
                "guest": guest,
                "too_late": False
                })
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @guest_ns.doc("remove_guest") 
    @login_required
    @admin_or_guest_required
    def delete(self, guest_id):
        """Delete a guest by ID"""
        try:
            guest_prov = get_guest(guest_id)
            event_prov = get_event(guest_prov["event"])
            if guest_prov["user"] == event_prov["organizer"]:
                return jsonify({"error": "The organizer can't be deleted"})
            delete_guest(guest_id)
            return jsonify({"message": "Guest deleted"})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@guest_ns.route("/items_for_a_guest/<int:guest_id>") 
class Assign(Resource):
    @guest_ns.doc("items_for_a_guest")
    @login_required
    @admin_or_guests_required
    def get(self, guest_id):
        """Get all items for a guest"""
        try:
            items = items_for_a_guest(guest_id)
            return jsonify(items)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})


@guest_ns.route("/all_guest/<int:user_id>") 
@guest_ns.param("user_id", "The user identifier") 
class AllGuest(Resource):
    @guest_ns.doc("get_full_all_guest")
    @login_required
    @admin_or_owner_required
    def get(self, user_id):
        """Get a guest by ID"""
        try:
            response = get_full_all_guest(user_id)
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})