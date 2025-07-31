import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    # Crear un nuevo usuario
    payload = {
        "first_name": "Ana",
        "last_name": "Lopez",
        "email": "ana@example.com"
    }
    response = client.post('/api/v1/users/', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['first_name'] == "Ana"
    assert 'id' in data

def test_duplicate_email(client):
    payload = {
        "first_name": "Ana",
        "last_name": "Lopez",
        "email": "ana@example.com"
    }
    client.post('/api/v1/users/', json=payload)
    response = client.post('/api/v1/users/', json=payload)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_get_users(client):
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_user_by_id(client):
    # Crear primero
    payload = {
        "first_name": "Carlos",
        "last_name": "Gomez",
        "email": "carlos@example.com"
    }
    create_response = client.post('/api/v1/users/', json=payload)
    user_id = create_response.get_json()['id']

    # Obtener por ID
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == "carlos@example.com"

def test_update_user(client):
    # Crear primero
    payload = {
        "first_name": "Luis",
        "last_name": "Martinez",
        "email": "luis@example.com"
    }
    create_response = client.post('/api/v1/users/', json=payload)
    user_id = create_response.get_json()['id']

    # Actualizar
    updated = {
        "first_name": "Luis",
        "last_name": "M.",
        "email": "luis@example.com"
    }
    update_response = client.put(f'/api/v1/users/{user_id}', json=updated)
    assert update_response.status_code == 200
    assert update_response.get_json()['last_name'] == "M."