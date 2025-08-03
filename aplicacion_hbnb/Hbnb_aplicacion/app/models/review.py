#!/usr/bin/python3
"""
in this module we define the class Review(), the template of the
future entitis of review
"""
from app.models.base_model import BaseModel, db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def update(self, data):
        for key in ['text', 'rating', 'place_id', 'user_id']:
            if key in data:
                setattr(self, key, data[key])
    
    def to_dict(self):
        base = super().to_dict()
        base.update ({
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
                    })
        return base