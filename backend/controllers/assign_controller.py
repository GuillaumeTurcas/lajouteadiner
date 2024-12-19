from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from models.assign import *
from auth import *
import json

# Assign namespace
assign_ns = Namespace("assigns", description="Assign related operations")

# Assign model for Swagger documentation
assign_model = assign_ns.model("Assign", {
    "guest": fields.Integer(required=True, description="Guest ID associated with the assignment"),
    "item": fields.Integer(required=True, description="Item ID to be assigned"),
    "quantity": fields.Integer(required=True, description="Quantity of the item assigned")
})

@assign_ns.route("/")
class AssignList(Resource):
    @assign_ns.doc("list_assigns")
    @login_required
    @admin_required
    def get(self): 
        """List all assignments"""
        try:
            assigns = get_assigns()
            return jsonify(assigns)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @assign_ns.expect(assign_model)
    @assign_ns.doc("add_assign")
    @login_required
    def post(self): 
        """Create a new assignment"""
        try:
            data = request.json
            if "item" in data:
                guest_list = get_guests_event(get_item(data["item"]).get("event"))
                is_guest = False
                for guest in guest_list:
                    if guest["user"] == session["user"]:
                        is_guest = True
                if is_guest or session["admin"] >= 1:
                    assign = create_assign(data["guest"], data["item"], data["quantity"]) if authorize(data) else None
                else:
                    return jsonify({"error": "You are not a guest or an admin to add an assign"})
            return jsonify(assign)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

@assign_ns.route("/<int:assign_id>")
@assign_ns.param("assign_id", "The assignment identifier")
class Assign(Resource):
    @assign_ns.doc("get_assign") 
    @login_required
    @admin_or_guests_required
    def get(self, assign_id): 
        """Get an assignment by ID"""
        try:
            assign = get_assign(assign_id)
            return jsonify(assign)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @assign_ns.expect(assign_model)
    @assign_ns.doc("modify_assign")
    @login_required
    @admin_or_guests_required
    def put(self, assign_id): 
        """Update an assignment by ID"""
        try:
            data = request.json
            assign = update_assign(assign_id, data)
            return jsonify(assign)
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})

    @assign_ns.doc("remove_assign")
    @login_required
    @admin_or_guest_required
    def delete(self, assign_id): 
        """Delete an assignment by ID"""
        try:
            delete_assign(assign_id)
            return jsonify({"message": "Assign deleted"})
        except Exception as e:
            return jsonify({"error": f"Error: {e}"})