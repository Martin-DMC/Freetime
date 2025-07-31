#!/usr/bin/python3
"""
in this module we define the class Review(), the template of the
future entitis of review
"""
from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

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