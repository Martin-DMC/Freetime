"""
in this module we define the BaseModel(),
like him name say, is the base of all models in
this package, her in charge of generate all id of
the different entities that inherit of her, save and
update all entities
"""
import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def to_dict(self):
        return {
        'id': self.id,
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat()
    }