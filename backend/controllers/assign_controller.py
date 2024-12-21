from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (JWTManager, create_access_token, 
    create_refresh_token, jwt_required, get_jwt_identity, 
    get_csrf_token, verify_jwt_in_request)
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
            verify_jwt_in_request() 
            current_user = json.loads(get_jwt_identity())   
            if "item" in data:
                guest_list = get_guests_event(get_item(data["item"]).get("event"))
                is_guest = False
                for guest in guest_list:
                    if guest["user"] == current_user["user_id"]:
                        is_guest = True
                if is_guest or current_user["admin"] >= 1:
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