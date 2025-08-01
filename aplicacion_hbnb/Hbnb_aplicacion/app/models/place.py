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

    amenities = db.relationship('Amenity', secondary='amenities', backref=db.backref('places', lazy='dynamic'))
    owner = db.relationship('User', backref='places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    #amenities = db.relationship('Amenity', secondary='place_amenity', backref='places', lazy='dynamic')

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
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        })
        return base

    def to_ubication(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }