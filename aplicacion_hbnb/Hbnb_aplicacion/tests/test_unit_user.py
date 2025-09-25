from app.models.user import User
from datetime import datetime
import bcrypt
import pytest

def test_create_user():
    first_name = 'pepe'
    last_name = 'argento'
    email = 'pepe@loco.com'

    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email

    assert 'pe' in user.first_name
    assert user.last_name == 'argento'

def test_try_to_dict():
    first_name = 'pepe'
    last_name = 'argento'
    email = 'pepe@loco.com'

    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.id = '1234-uuid'
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()

    info = user.to_dict()

    assert isinstance(info, dict)
    assert 'id' in info
    assert 'first_name' in info
    assert user.email == 'pepe@loco.com'
    assert 'created_at' in info

class MockUser:
    def __init__(self, contraseña):
        self.contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        if not self.contraseña_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),self.contraseña_hash)

@pytest.fixture
def mock_user():
    return MockUser("mi_contraseña_secreta")

def test_hash_password(mock_user):
    assert mock_user.contraseña_hash is not None
    assert isinstance(mock_user.contraseña_hash, bytes)
    assert len(mock_user.contraseña_hash) > 0

def test_verifity_password_correcta(mock_user):
    assert mock_user.verify_password("mi_contraseña_secreta") is True

def test_verify_password_incorrecta(mock_user):
    assert mock_user.verify_password("contraseña_incorrecta") is False

def test_verify_password_sin_hash():
    user = MockUser("otra-contraseña")
    user.contraseña_hash = b''
    assert user.verify_password("otra-contraseña") is False