#!/usr/bin/python3
"""
in this module we define the class Amenity(). the template
of all future instances
"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, place_id=None):
        super().__init__()
        if len(name) < 50:
            self.name = name
        else:
            self.name = None
        self.place_id = place_id

    def to_dict(self):
        base = super().to_dict()
        base.update ({
            'name': self.name,
            'place_id': self.place_id
        })
        
        return base