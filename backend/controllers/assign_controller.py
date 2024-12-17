from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from models.assign import *
import json

# Assign namespace
assign_ns = Namespace('assigns', description='Assign related operations')

# Assign model for Swagger documentation
assign_model = assign_ns.model('Assign', {
    'guest': fields.Integer(required=True, description='Guest ID associated with the assignment'),
    'item': fields.Integer(required=True, description='Item ID to be assigned'),
    'quantity': fields.Integer(required=True, description='Quantity of the item assigned')
})

@assign_ns.route('/')
class AssignList(Resource):
    @assign_ns.doc('list_assigns')
    def get(self):
        """List all assignments"""
        assigns = get_assigns()
        return jsonify(assigns)

    @assign_ns.expect(assign_model)
    @assign_ns.doc('add_assign')
    def post(self):
        """Create a new assignment"""
        data = request.json
        assign = create_assign(data['guest'], data['item'], data['quantity'])
        return jsonify(assign)

@assign_ns.route('/<int:assign_id>')
@assign_ns.param('assign_id', 'The assignment identifier')
class Assign(Resource):
    @assign_ns.doc('get_assign')
    def get(self, assign_id):
        """Update an assignment by ID"""
        assign = get_assign(assign_id)
        return jsonify(assign)
    @assign_ns.expect(assign_model)
    @assign_ns.doc('modify_assign')
    def put(self, assign_id):
        """Update an assignment by ID"""
        data = request.json
        assign = update_assign(assign_id, data)
        return jsonify(assign)

    @assign_ns.doc('remove_assign')
    def delete(self, assign_id):
        """Delete an assignment by ID"""
        delete_assign(assign_id)
        return jsonify({'message': 'Assign deleted'})


