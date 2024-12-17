from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from models.guest import *

# Guest namespace
guest_ns = Namespace('guests', description='Guest related operations')

# Guest model for Swagger documentation
guest_model = guest_ns.model('Guest', {
    'user': fields.Integer(required=True, description='User ID of the guest'),
    'event': fields.Integer(required=True, description='Event ID the guest is assigned to')
})

@guest_ns.route('/')
class GuestList(Resource):
    @guest_ns.doc('list_guests')
    def get(self):
        """List all guests"""
        guests = get_guests()
        return jsonify(guests)

    @guest_ns.expect(guest_model)
    @guest_ns.doc('add_guest')
    def post(self):
        """Create a new guest"""
        data = request.json
        guest = create_guest(data['user'], data['event'])
        return jsonify(guest)

@guest_ns.route('/<int:guest_id>')
@guest_ns.param('guest_id', 'The guest identifier')
class Guest(Resource):
    @guest_ns.doc('get_guest')
    def get(self, guest_id):
        """Get a guest by ID"""
        guest = get_guest(guest_id)
        return jsonify(guest)

    @guest_ns.doc('accept_guest')
    def post(self, guest_id):
        """A guest change his decision to go to an event"""
        guest = accept_guest(guest_id)
        return jsonify(guest)

    @guest_ns.doc('remove_guest')
    def delete(self, guest_id):
        """Delete a guest by ID"""
        delete_guest(guest_id)
        return jsonify({'message': 'Guest deleted'})

@guest_ns.route('/items_for_a_guest/<int:guest_id>')
class Assign(Resource):
    @guest_ns.doc('items_for_a_guest')
    def get(self, guest_id):
        """Update an assignment by ID"""
        items = items_for_a_guest(guest_id)
        return jsonify(assign)
