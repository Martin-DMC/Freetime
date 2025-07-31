import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['first_name'], "Jane")

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

        self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com"
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testt.user@example.com"
        })
        user_id = response.json['id']

        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "pepe",
            "last_name": "quintero",
            "email": "pepe.quintero@ejemplo.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], "pepe")
        self.assertEqual(response.json['last_name'], "quintero")
        self.assertEqual(response.json['email'], "pepe.quintero@ejemplo.com")