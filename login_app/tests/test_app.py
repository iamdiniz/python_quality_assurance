import pytest
from pytest import mark
from app import app, db, User
from werkzeug.security import generate_password_hash

# Fixture for setting up a test client and environment
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use SQLite in-memory database for testing
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing purposes

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables for testing
        yield client
        with app.app_context():
            db.drop_all()  # Clean up the database after testing

# Teste de Rota: Verifica se a página inicial requer login
@mark.home
def test_home_requires_login(client):
    response = client.get('/home')  # Tenta acessar a rota home sem logar
    assert response.status_code == 401  # Espera-se um status 401 Unauthorized

# Teste unitario
def validate_name(name):
    if name[0].isdigit():
        return False, "The name cannot start with a number."
    return True, ""

@mark.validname
def test_validate_name():
    valid_name = "John Doe"
    invalid_name = "1John"

    assert validate_name(valid_name) == (True, "")  # Espera-se que o nome válido retorne True
    assert validate_name(invalid_name) == (False, "The name cannot start with a number.")  # Espera-se que o nome inválido retorne False
