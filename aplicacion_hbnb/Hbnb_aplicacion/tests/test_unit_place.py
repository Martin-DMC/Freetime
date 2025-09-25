from app.models.place import Place
from app.models.base_model import BaseModel
from datetime import datetime
from unittest.mock import MagicMock, patch, Mock
import pytest 

class DummyAmenity:
    def __init__(self, name):
        self.name = name

class DummyReview:
    def __init__(self, text):
        self.text = text

def test_crear_lugar_sin_db():
    # Asume que Place es una clase simple, sin necesidad de conectarse a la DB para la instancia
    title = 'apartamento'
    description = 'lindo apart bro'
    price = 120.0
    
    # Creamos una instancia del modelo sin pasar por la lógica de la DB
    place = Place()
    place.title = title
    place.description = description
    place.price = price

    # Verificamos los atributos directamente
    assert place.title == 'apartamento'
    assert place.description == 'lindo apart bro'
    assert place.price == 120.0

@patch('app.models.place.Place.reviews', new_callable=MagicMock)
def test_add_review(mock_reviews):
    place = Place()
    mock_review = MagicMock()

    place.add_review(mock_review)

    mock_reviews.append.assert_called_once_with(mock_review)

@patch('app.models.place.Place.amenities', new_callable=MagicMock)
def test_add_and_remove_review(mock_amenities):
    place = Place()
    mock_amenity = MagicMock()

    place.add_amenity(mock_amenity)

    mock_amenities.append.assert_called_once_with(mock_amenity)

    place.remove_amenity(mock_amenity)

    mock_amenities.remove.assert_called_once_with(mock_amenity)

def test_try_to_dict():
    title = 'apartamento'
    price = 120.0

    place = Place()
    place.title = title
    place.price = price
    place.id = '1234-uuid'
    place.created_at = datetime.utcnow()
    place.updated_at = datetime.utcnow()

    to_dict = place.to_dict()

    assert isinstance(to_dict, dict)
    assert 'title' in to_dict
    assert 'price' in to_dict

def test_try_to_ubication():
    title = 'apartamento'
    price = 120.0
    latitude = 34.444
    longitude = 33.234

    place = Place()
    place.title = title
    place.price = price
    place.latitude = latitude
    place.longitude = longitude

    ubicacion = place.to_ubication()

    assert isinstance(ubicacion, dict)
    assert 'latitude' in ubicacion
    assert 'longitude' in ubicacion

@patch('app.models.place.Place.amenities', new_callable=MagicMock)
@patch('app.models.place.Place.reviews', new_callable=MagicMock)
@patch('app.models.place.Place.owner', new_callable=MagicMock)
@patch('app.models.base_model.BaseModel.to_dict') # Esto mockea el super().to_dict()
def test_try_to_full_info(mock_to_dict, mock_owner, mock_reviews, mock_amenities):
    """
    Testea la función to_full_info simulando todas las dependencias.
    """
    # 1. Configurar los mocks
    # Configurar lo que super().to_dict() debería devolver
    mock_to_dict.return_value = {
        'id': 'mock-id-123',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    # Crear mocks para owner, amenities y reviews
    mock_owner.to_dict.return_value = {
        'id': 'owner-id',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    
    mock_amenity_1 = MagicMock()
    mock_amenity_1.to_dict.return_value = {
        'id': 'a1',
        'name': 'Pool'
    }
    mock_amenity_2 = MagicMock()
    mock_amenity_2.to_dict.return_value = {
        'id': 'a2',
        'name': 'WiFi'
    }
    mock_amenities.__iter__.return_value = [mock_amenity_1, mock_amenity_2]
    
    mock_review_1 = MagicMock()
    mock_review_1.to_dict.return_value = {
        'id': 'r1',
        'text': 'Great place!'
    }
    mock_reviews.__iter__.return_value = [mock_review_1]

    # 2. Instanciar la clase y asignar los mocks como atributos
    place = Place()
    place.title = 'apartamento'
    place.price = 120.0
    place.id = '1234-uuid'
    
    # Asigna directamente los objetos mock a los atributos de la instancia
    place.owner = mock_owner
    place.amenities = mock_amenities
    place.reviews = mock_reviews
    
    # Llama a la función que queremos probar
    full_info = place.to_full_info()
    
    # 3. Assertions (Verificaciones)
    # Verifica que la función devolvió un diccionario con los datos correctos
    assert isinstance(full_info, dict)
    assert full_info['owner'] == {'id': 'owner-id', 'first_name': 'John', 'last_name': 'Doe'}
    assert full_info['amenities'] == [{'id': 'a1', 'name': 'Pool'}, {'id': 'a2', 'name': 'WiFi'}]
    assert full_info['reviews'] == [{'id': 'r1', 'text': 'Great place!'}]

    # Verificamos que los mocks fueron llamados
    mock_to_dict.assert_called_once()
    mock_owner.to_dict.assert_called_once()
    mock_amenity_1.to_dict.assert_called_once()
    mock_amenity_2.to_dict.assert_called_once()
    mock_review_1.to_dict.assert_called_once()
