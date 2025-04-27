from flask import Flask, render_template, redirect, url_for, session, request
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "una_clave_segura")

google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def home():
    if not google.authorized:
        return redirect(url_for("login"))
    return redirect(url_for("test_step", step=1))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/test/<int:step>")
def test_step(step):
    if not google.authorized:
        return redirect(url_for("login"))
    # Capture gender on step1
    if step == 2:
        gender = request.args.get('gender')
        if gender in ['male', 'female', 'other']:
            session['user_gender'] = gender
    if 1 <= step <= 5:
        return render_template(f"step{step}.html", current_step=step)
    return redirect(url_for("chat"))

@app.route("/chat")
def chat():
    if not google.authorized:
        return redirect(url_for("login"))
    # Determine avatar based on stored gender
    gender = session.get('user_gender', 'other')
    if gender == 'male':
        avatar_file = 'avatar_female.png'
    elif gender == 'female':
        avatar_file = 'avatar_male.png'
    else:
        avatar_file = 'avatar_andro.png'
    avatar_url = url_for('static', filename='assets/' + avatar_file)
    return render_template('chat.html', avatar_url=avatar_url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
