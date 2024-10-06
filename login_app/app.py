import re
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'daa351b615c916ff50121245a9f807b9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234567@localhost/training'

db = SQLAlchemy(app)

class Userr(db.Model):
    __tablename__ = 'userr'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

# Criação da tabela se não existir
with app.app_context():
    db.create_all()

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Userr.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Verifica se o nome começa com um número
        if name[0].isdigit():
            flash('O nome não pode começar com um número.', 'danger')
            return redirect(url_for('register'))
        
        # Verifica se o email já está registrado
        if Userr.query.filter_by(email=email).first():
            flash('Endereço de email já existe.', 'danger')
            return redirect(url_for('register'))

        # Valida o formato do email
        if not validate_email(email):
            flash('Formato de email inválido.', 'danger')
            return redirect(url_for('register'))

        # Valida a senha
        if len(password) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        new_user = Userr(name=name, email=email, password=password_hash)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Conta criada com sucesso! Por favor, faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Ocorreu um erro ao criar sua conta. Por favor, tente novamente.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

def validate_email(email):
    import re
    # Valida se o email possui o formato correto
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

@app.route("/home")
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)