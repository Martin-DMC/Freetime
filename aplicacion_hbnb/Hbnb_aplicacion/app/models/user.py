#!/usr/bin/python3
"""
in this module we define the class User(), the template
of all future entities
"""

from app.models.base_model import BaseModel, db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    contraseña_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    places = db.relationship('Place', back_populates='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')

    # defino la clase user()
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            if key == 'contraseña' and value:
                self.hash_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)

    def hash_password(self, contraseña):
        """Hashes the password before storing it."""
        self.contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if self.contraseña_hash:
            return bcrypt.check_password_hash(self.contraseña_hash, password)
        return False

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'places_count': len(self.places)
        })
        return base