import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Ativar modo de teste
    with app.test_client() as client:
        yield client

def test_index_route():
    response = app.test_client().get('/login')

    assert response.status_code == 200

def test_register_name_starts_with_number(client):
    # Dados de teste
    data = {
        'name': '1Nome',
        'email': 'teste@example.com',
        'password': 'senha123'
    }
    
    # Realiza a requisição POST para a rota /register
    response = client.post('/register', data=data)  # Mudei para `data=data` em vez de `json=data`
    
    # Verifica se a resposta contém a mensagem correta
    assert response.status_code == 400
    assert response.get_json()['message'] == "The name cannot start with a number."
