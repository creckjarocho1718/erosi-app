from flask import Flask, render_template, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia_esto_por_una_clave_segura")

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
    if 1 <= step <= 4:
        return render_template(f"step{step}.html")
    return redirect(url_for("chat"))

@app.route("/chat")
def chat():
    if not google.authorized:
        return redirect(url_for("login"))
    return render_template("chat.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
