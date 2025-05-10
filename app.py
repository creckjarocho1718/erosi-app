import os
from flask import Flask, render_template, session, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

# Inicialización
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# Google OAuth
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    return redirect(url_for("chat"))

@app.route("/chat")
def chat():
    avatar = session.get("avatar", "male")
    return render_template(
        "chat.html",
        avatar_video=f"{avatar}_loop.webm",
        avatar_speaking=f"{avatar}_loop.webm"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
