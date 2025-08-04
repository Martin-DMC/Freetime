"""
in this module we define and handler all about the data received
of the client since the diferents routes of our web app
"""


from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, min_length=1, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Ubication already registred')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload

        current_user_id = get_jwt_identity()
        place_data['owner_id'] = current_user_id

        # Validar campos esenciales
        required_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                return {'error': f"Missing required field: {field}"}, 400

        # Validar que el owner_id exista
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            return {'error': 'Owner_id does not exist'}, 400
        
        # Verificar si la ubicación ya está registrada
        existing_coords = facade.get_places_ubis()
        ubication = {
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude']
        }
        if ubication in existing_coords:
            return {'error': 'Ubication already registered'}, 400

        new_place = facade.create_place(place_data)

        if 'error' in new_place:
            return new_place, 400
        return new_place, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200

    @api.response(404, 'Place not found')
    @api.response(403, 'Permission denied')
    @api.response(200, 'Place deleted successfully')
    @jwt_required()
    def delete(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        current_user_id = get_jwt_identity()
        if current_user_id != place.owner_id:
            return {'error': 'no autorizado'}, 403
        retorno, estado = facade.delete_place(place_id)
        return retorno, estado


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Permission denied')
    @api.response(500, 'Internal server error')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        update_data = api.payload

        # Buscar el lugar por ID
        place = facade.place_repo.get(place_id)  # ← Es importante que sea el objeto, no un dict
        if place is None:
            return {'error': 'Place not found'}, 404
        
        current_user_id = get_jwt_identity()
        if current_user_id != place.owner_id:
            return {'error': 'no autorizado'}, 403

        # No permitir modificar latitud ni longitud
        if 'latitude' in update_data and update_data['latitude'] != place.latitud:
            return {'error': "Location (latitude) cannot be modified"}, 400
        if 'longitude' in update_data and update_data['longitude'] != place.longitud:
            return {'error': "Location (longitude) cannot be modified"}, 400

        # Validar que el nuevo owner_id exista si se quiere cambiar
        if 'owner_id' in update_data and update_data['owner_id'] != place.owner_id:
            if not facade.get_user(update_data['owner_id']):
                return {'error': "New owner_id does not exist"}, 400

        # Hacer la actualización
        updated_place = facade.update_place(place_id, update_data)

        if updated_place:
            return updated_place if isinstance(updated_place, dict) else updated_place.to_dict(), 200

        return {'error': 'Internal server error'}, 500

@api.route('/<place_id>/amenities')
class PlaceAmenityAssociation(Resource):
    @api.response(201, 'Amenity associated successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Place or Amenity not found')
    @jwt_required()
    def post(self, place_id):
        """Asocia una amenidad existente con un lugar."""
        amenity_data = api.payload
        amenity_name = amenity_data.get('name')

        if not amenity_name:
            return {'error': 'Amenity name is required'}, 400

        try:
            facade.associate_amenity_with_place(place_id, amenity_name)
            return {'message': 'Amenity associated with place'}, 201

        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 500