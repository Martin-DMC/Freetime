#!/usr/bin/python3
"""
in this module we define the class Place(),
the template of the future places in our app.
"""
from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitud = latitude
        self.longitud = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'title': self.title,
            'latitude': self.latitud,
            'longitude': self.longitud,
            'owner_id': self.owner_id
        })
        return base

    def to_ubication(self):
        return {
            'latitude': self.latitud,
            'longitude': self.longitud
        }