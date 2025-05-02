from flask import Flask, render_template, redirect, url_for, session, request, jsonify, send_file
from flask_dance.contrib.google import make_google_blueprint, google
import os, openai, io
from gtts import gTTS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "una_clave_segura")
openai.api_key = os.environ.get("OPENAI_API_KEY")

google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
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
        return render_template(f"step{step}.html", current_step=step)
    if step == 5:
        return render_template("step5.html")
    return redirect(url_for("chat"))

@app.route("/set_avatar/<choice>")
def set_avatar(choice):
    if choice in ['male', 'female', 'other']:
        session['avatar_choice'] = choice
    return redirect(url_for("chat"))

@app.route("/chat")
def chat():
    if not google.authorized:
        return redirect(url_for("login"))
    choice = session.get('avatar_choice', 'male')
    avatar_map = {
        'male': 'avatar_male_loop.webm',
        'female': 'avatar_female_loop.webm',
        'other': 'avatar_andro_loop.webm'
    }
    avatar_video = avatar_map.get(choice, 'avatar_male_loop.webm')
    return render_template("chat.html", avatar_video=avatar_video)

@app.route("/api/message", methods=["POST"])
def api_message():
    data = request.get_json()
    user_msg = data.get("message", "")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Dr. Erosi, professional yet playful sexual education AI."},
            {"role": "user", "content": user_msg}
        ]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

@app.route("/api/tts")
def api_tts():
    text = request.args.get("text", "")
    tts = gTTS(text=text, lang="es")
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return send_file(buf, mimetype="audio/mpeg")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
