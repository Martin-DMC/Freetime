"""
In this module we define the logic of how our facade works,
the connection with the 'database', and the responses to the API.
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review



class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # =================== USERS ===================
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user.to_dict()

    def get_users(self):
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, update_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(update_data)
            return user.to_dict()
        return None

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # =================== AMENITIES ===================
    def create_amenity(self, amenity_data):
        place_id = amenity_data.get('place_id')
        if not place_id or not self.place_repo.get(place_id):
            return {'error': 'Invalid or missing place_id'}

        amenity = Amenity(name=amenity_data['name'], place_id=place_id)
        self.amenity_repo.add(amenity)
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            return amenity.to_dict()
        return None

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity.to_dict()
        return None

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)

    # =================== PLACES ===================
    def create_place(self, place_data):
        price = place_data['price']
        lat = place_data['latitude']
        lon = place_data['longitude']

        # Validaciones básicas
        if price < 0:
            raise ValueError('Invalid price')
        if not -90.0 <= lat <= 90.0:
            raise ValueError('Invalid latitude')
        if not -180.0 <= lon <= 180.0:
            raise ValueError('Invalid longitude')
        
        # Validar existencia de usuario
        owner_id = place_data['owner_id']
        owner = self.user_repo.get(owner_id)
        if not owner:
            return {'error': 'owner_id not found'}

        place = Place(**place_data)
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        amenities = self.amenity_repo.get_by_place_id(place_id)

        place_dict = place.to_dict()
        place_dict['amenities'] = [
            {'id': amenity.id, 'name': amenity.name} for amenity in amenities
        ] if amenities else []

        return place_dict

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def add_amenities(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id['id'])
        return place.add_amenity(amenity)


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
            return place.to_dict()
        return None

    def get_places_ubis(self):
        places = self.place_repo.get_all()
        return [place.to_ubication() for place in places]

    def add_amenity_to_place(self, place_id, amenity_data):
        place = self.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}

        
        amenity = Amenity(name=amenity_data['name'], place_id=place_id)
        self.amenity_repo.add(amenity)

        return amenity.to_dict()

    # =================== REVIEWS ===================
    def create_review(self, review_data):
        if 'text' not in review_data or not review_data['text']:
            raise ValueError("Review text is required.")

        raw_rating = review_data.get('rating')
        try:
            rating = float(str(raw_rating).replace(',', '.'))
        except (ValueError, TypeError):
            raise ValueError("Valid rating is required.")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user or not place:
            raise ValueError("Invalid user_id or place_id.")

        review = Review(
            text=review_data['text'],
            rating=rating,
            user_id=user.id,
            place_id=place.id
        )

        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        print(f"Place encontrado: {place}")
        if not place:
            raise ValueError("Place not found.")

        reviews = self.review_repo.get_reviews_by_place(place_id)
        print(f"Reviews encontradas: {reviews}")
        return [review.to_dict() for review in reviews]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")

        if 'text' in review_data:
            review.text = review_data['text']

        if 'rating' in review_data:
            try:
                rating = float(str(review_data['rating']).replace(',', '.'))
            except (ValueError, TypeError):
                raise ValueError("Valid rating is required.")
    
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            review.rating = rating

        self.review_repo.update(review.id, review_data)
        return review.to_dict()

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")

        reviews = self.review_repo.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")

        if 'text' in review_data:
            review.text = review_data['text']

        if 'rating' in review_data:
            try:
                rating = float(str(review_data['rating']).replace(',', '.'))
            except (ValueError, TypeError):
                raise ValueError("Valid rating is required.")
        
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            review.rating = rating

        self.review_repo.update(review, review_data)
        return review.to_dict()

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}