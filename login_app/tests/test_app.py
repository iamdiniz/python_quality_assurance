import pytest
from pytest import mark
from app import app, db, User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use um banco de dados SQLite persistente
    app.config['WTF_CSRF_ENABLED'] = False  # Desabilitar CSRF para fins de teste

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Cria todas as tabelas para testes
        yield client

# Teste de Rota: Verifica se a página inicial requer login
@mark.home
def test_deve_retornar_302_quando_acessar_home_sem_logar(client):
    response = client.get('/home')  # Tenta acessar a rota home sem logar
    assert response.status_code == 302  # Espera-se um status 401 Unauthorized

@mark.login
def test_rota_login_deve_ser_acessivel(client):
    response = client.get('/login')
    assert response.status_code == 200  # Verifica se o status é 200 (OK)
    assert b'Login' in response.data  # Verifica se a página contém o texto "Login"

# Teste unitario
def validar_nome(name):
    if name[0].isdigit():
        return False, "The name cannot start with a number."
    return True, ""

@mark.validname
def test_deve_retornar_mensagem_de_erro_ao_inserir_nome_com_numero():
    valid_name = "John Doe"
    invalid_name = "1John"

    assert validar_nome(valid_name) == (True, "")  # Espera-se que o nome válido retorne True
    assert validar_nome(invalid_name) == (False, "The name cannot start with a number.")  # Espera-se que o nome inválido retorne False

@mark.create
def test_deve_criar_usuario_com_sucesso():
    # Criação de um usuário manualmente
    user = User(name="Guilherme", email="guilherme@gmail.com", password=generate_password_hash("12345678"))
    
    # Testar se o usuário foi criado corretamente
    assert user.name == "Guilherme"
    assert user.email == "guilherme@gmail.com"
    assert user.password != "12345678"  # Senha deve estar hasheada

# Testes de Integração focam no fluxo de trabalho completo, como o processo de login e registro.
@mark.integration
def test_registrar_e_login_deve_ser_bem_sucedido_com_dados_validos(client):
    # Teste de registro
    register_data = {
        'name': 'Bruno',
        'email': 'bruno@gmail.com',
        'password': '12345678'
    }
    
    # Envia os dados de registro
    response = client.post('/register', data=register_data, follow_redirects=True)

    # Teste de login
    login_data = {
        'email': 'bruno@gmail.com',
        'password': '12345678'
    }
    
    # Envia os dados de login
    response = client.post('/login', data=login_data, follow_redirects=True)
    
    # Verifica se o login foi bem-sucedido redirecionando para a página inicial
    assert response.status_code == 200  # A página inicial deve retornar 200 (OK)
    assert b'Welcome to Quality Assurance Dashboard' in response.data  # Verifica se a mensagem de boas-vindas está presente

    # Verifica se a sessão contém o ID do usuário
    with client.session_transaction() as session:
        assert 'user_id' in session  # Verifica se o ID do usuário foi armazenado na sessão

@pytest.mark.api
def test_get_users_retorna_usuarios(client):
    # Fazer uma requisição GET para a rota /api/users
    response = client.get('/api/users')
    
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    
    # Verifica se o conteúdo retornado contém o usuário inserido
    data = response.get_json()  # Converte a resposta para JSON
    assert len(data) > 0  # Verifica se pelo menos um usuário foi retornado
    assert data[0]['name'] == "Guilherme"  # Verifica se o nome do primeiro usuário é o esperado
    assert data[0]['email'] == "guilherme@gmail.com"  # Verifica o email do usuário
    
# comando para gerar report: pytest --junitxml nome.xml