#!/usr/bin/python3
"""
in this module we define the class Place(),
the template of the future places in our app.
"""
from app.models.base_model import BaseModel, db

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    amenities = db.relationship('Amenity', secondary='place_amenity_association', back_populates='places')
    owner = db.relationship('User', back_populates='places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.remove(amenity)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'id': self.id,
            'title': self.title,
            'price': self.price
        })
        return base

    def to_ubication(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def to_full_info(self):
        base = super().to_dict()
        base.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': [a.to_dict() for a in self.amenities],
            'reviews': [r.to_dict() for r in self.reviews]
        })
        return base