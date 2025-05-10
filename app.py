# Importar los módulos necesarios de Flask
from flask import Flask, render_template, redirect, session, url_for
import os

# Inicializar la aplicación Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    return render_template('login.html', client_id=client_id)

@app.route('/test')
def test_list():
    avatars_dir = os.path.join(app.static_folder, 'assets/avatars')
    avatars = [f for f in os.listdir(avatars_dir) if os.path.isfile(os.path.join(avatars_dir, f))]
    return render_template('test_list.html', avatars=avatars)

@app.route('/test/<avatar>')
def test(avatar):
    session['avatar'] = avatar
    return render_template('test.html', avatar=avatar)

@app.route('/chat')
def chat():
    avatar = session.get('avatar', None)
    return render_template('chat.html', avatar=avatar)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
