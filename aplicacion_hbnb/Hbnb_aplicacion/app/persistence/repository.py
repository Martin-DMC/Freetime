"""
in this module we define what would
be the improvise data base
"""
from abc import ABC, abstractmethod
from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import User, Place, Review, Amenity
from app.models.amenity import place_amenity_association

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

    def get_by_place_id(self, place_id):
        return [
            obj for obj in self._storage.values()
            if getattr(obj, 'place_id', None) == place_id
                ]
    
    def get_reviews_by_place(self, place_id):
        return [
        obj for obj in self._storage.values()
        if getattr(obj, 'place_id', None) == place_id
        ]


"""----------------------------------------------
                    BASE DE DATOS
---------------------------------------------------"""

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).all()
    
    def get_by_place_id(self, place_id):
        amenities = db.session.query(Amenity).join(place_amenity_association,\
                Amenity.id == place_amenity_association.c.amenity_id).\
                filter(place_amenity_association.c.place_id == place_id).all()
        return amenities

    def get_reviews_by_place(self, place_id):
        reviews = db.session.query(Review).filter(Review.place_id == place_id).all()
        return reviews

