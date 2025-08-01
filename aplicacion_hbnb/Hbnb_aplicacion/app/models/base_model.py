"""
in this module we define the BaseModel(),
like him name say, is the base of all models in
this package, her in charge of generate all id of
the different entities that inherit of her, save and
update all entities
"""
import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    """
    importamos la instancia de db para hacer que la basemodel herede
    de db.Model
    """
    __abstract__ = True  # le decimos a db que no cree una tabla para esta clase

    # conecto la base de datos con la BaseModel
    # elimino el init por que ahora estas definiciones hacen su trabajo 
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def to_dict(self):
        return {
        'id': self.id,
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat()
    }