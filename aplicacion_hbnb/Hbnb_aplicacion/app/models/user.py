#!/usr/bin/python3
"""
in this module we define the class User(), the template
of all future entities
"""

from app.models.base_model import BaseModel

class User(BaseModel):
    # defino la clase user()
    def __init__(self, first_name: str, last_name: str, email: str, contraseña=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._contraseña = contraseña
        self.is_admin = False
        self.owned_places = []

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        })
        return base