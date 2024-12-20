from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from models.item import *
from models.event import *
from auth import *
import json

item_ns = Namespace("items", description="Item related operations")

# Item model for Swagger documentation
item_model = item_ns.model("Item", {
    "name": fields.String(required=True, description="Name of the item"),
    "quantity": fields.Integer(required=True, description="Quantity of the item"),
    "description": fields.String(required=False, description="Description of the item"),
    "event": fields.Integer(required=True, description="Event ID associated with the item")
})

item_event_model = item_ns.model("ItemEvent", {
    "event_id": fields.Integer(required=True, description="Event ID to filter items")
})

@item_ns.route("/")
class ItemList(Resource):
    @item_ns.doc("list_items")
    @login_required
    @admin_required
    def get(self):
        """List all items"""
        try:
            items = get_items()
            return jsonify(items)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @item_ns.expect(item_model)
    @item_ns.doc("add_item")
    @login_required
    def post(self): 
        """Create a new item"""
        try:

            data = request.json
            verify_jwt_in_request()  # Vérifie que le JWT est valide
            current_user = json.loads(get_jwt_identity())
            
            if "event" in data:
                if get_event(data["event"]) \
                    .get("organizer") == current_user["user_id"] \
                    or current_user["admin"] >= 1:
                    item = create_item(data["name"], \
                        data["quantity"], data["description"], \
                        data["event"])
                else:
                    return jsonify({"error": "You are not the organizer or an admin to add an item"})
            return jsonify(item)
        except:
            return jsonify({"error": "Impossible to create a new item"})

@item_ns.route("/<int:item_id>")
@item_ns.param("item_id", "The item identifier")
class Item(Resource):
    @item_ns.expect(item_model)
    @item_ns.doc("modify_item")
    @login_required
    @admin_or_organizer_required
    def put(self, item_id):
        """Update an item by ID"""
        try:
            data = request.json
            item = update_item(item_id, data)
            return jsonify(item)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @item_ns.doc("remove_item")
    @login_required
    @admin_or_organizer_required
    def delete(self, item_id):
        """Delete an item by ID"""
        try:
            delete_item(item_id) 
            return jsonify({"message": "Item deleted"})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@item_ns.route("/event/<int:event_id>")
@item_ns.param("event_id", "The event identifier")
class ItemsByEvent(Resource):
    @item_ns.doc("items_user")
    @login_required
    @admin_or_guests_required
    def get(self, event_id):
        """List items by event ID"""
        try:
            items = get_items_event(event_id)
            return jsonify(items)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})
