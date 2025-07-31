"""
in this module we define and handler all about the data received
of the client since the diferents routes of our web app
"""


from flask_restx import Namespace, Resource, fields
from app.services import facade
import re

api = Namespace('users', description='User operations')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email_format(email):
    if not EMAIL_REGEX.match(email):
        raise ValueError('Formato de correo electrónico inválido.')
    return email

user_model = api.model('User', {
    'first_name': fields.String(required=True, min_length=1, description='First name of the user'),
    'last_name': fields.String(required=True, min_length=1, description='Last name of the user'),
    'email': fields.String(required=True, min_length=1, description='Email of the user', validate=validate_email_format)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return new_user, 201

    @api.response(200, 'all users')
    def get(self):
        users = facade.get_users()
        return users, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.response(200, 'User update successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        updated_data = api.payload
        updated_user = facade.update_user(user_id, updated_data)

        if updated_user:
            return updated_user, 200
        return {'error': 'User not found'}, 404


    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        try:
            facade.delete_user(user_id)
            return {'message': 'User deleted successfully'}, 200
        except ValueError:
            return {'error': 'User not found'}, 404
        