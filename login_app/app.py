from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'daa351b615c916ff50121245a9f807b9' # Essa chave é necessária para o uso de sessões e para que o sistema de flash funcione corretamente.

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica para verificar credenciais de login
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)