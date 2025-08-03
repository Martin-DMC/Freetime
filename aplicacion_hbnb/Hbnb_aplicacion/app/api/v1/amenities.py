"""
in this module we define and handler all about the data received
of the client since the diferents routes of our web app
"""


from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Modelo para crear amenity (POST) con place_id obligatorio
amenity_create_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'place_id': fields.String(required=True, description='ID of the place associated')
})

# Modelo para actualizar amenity (PUT) solo name obligatorio
amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_create_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def post(self):
        amenity_data = api.payload
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'].strip())
        if existing_amenity:
            return {'error': 'Amenity already registered'}, 400

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity, 200

    @api.expect(amenity_update_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        updated_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, updated_data)
        if updated_amenity:
            return updated_amenity, 200
        return {'error': 'Amenity not found'}, 404