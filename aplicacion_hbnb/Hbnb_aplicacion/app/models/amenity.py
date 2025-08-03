#!/usr/bin/python3
"""
in this module we define the class Amenity(). the template
of all future instances
"""
from app.models.base_model import BaseModel, db


place_amenity_association = db.Table(
    'place_amenity_association',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    places = db.relationship('Place', secondary=place_amenity_association, back_populates='amenities')

    def to_dict(self):
        base = super().to_dict()
        base.update ({
            'name': self.name
        })
        
        return base