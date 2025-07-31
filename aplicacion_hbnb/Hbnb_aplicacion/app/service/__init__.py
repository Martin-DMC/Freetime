"""
in this module we do to be start the facade pattern of our app,
this pattern in charge of handler all connections between
the layers in our app
"""
from app.services.facade import HBnBFacade

facade = HBnBFacade()