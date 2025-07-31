from flask_restx import Namespace, Resource, fields
from app.services import facade

places_ns = Namespace('places', description='Place operations')
api = Namespace('reviews', description='Review operations')


review_create_model = api.model('ReviewCreate', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Float(required=True, description='Rating of the place (1.0 - 5.0)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Float(required=False, description='Rating of the place (1.0 - 5.0)')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_model, validate=True)
    @api.response(201, 'Review successfully created / Reseña creada exitosamente')
    @api.response(400, 'Invalid input data / Datos de entrada no válidos')
    def post(self):
        review_data = api.payload
        try:
            review_data['rating'] = float(str(review_data['rating']).replace(',', '.'))
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully / Lista de reseñas recuperada exitosamente')
    def get(self):
        reviews = facade.get_all_reviews()
        return reviews, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully / Detalles de la reseña recuperados exitosamente')
    @api.response(404, 'Review not found / Reseña no encontrada')
    def get(self, review_id):
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError:
            return {'error': 'Review not found'}, 404

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully / Reseña actualizada exitosamente')
    @api.response(404, 'Review not found / Reseña no encontrada')
    @api.response(400, 'Invalid input data / Datos de entrada no válidos')
    def put(self, review_id):
        review_data = api.payload
        try:
            if 'rating' in review_data:
                review_data['rating'] = float(str(review_data['rating']).replace(',', '.'))
            updated_review = facade.update_review(review_id, review_data)
            return updated_review, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully / Reseña eliminada exitosamente')
    @api.response(404, 'Review not found / Reseña no encontrada')
    def delete(self, review_id):
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404


@places_ns.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @places_ns.response(200, 'List of reviews for the place retrieved successfully')
    @places_ns.response(404, 'Place not found')
    def get(self, place_id):
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return reviews, 200
        except ValueError:
            return {'error': 'Place not found'}, 404