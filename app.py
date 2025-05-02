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
    # Capture gender selection on step1
    if step == 2:
        gender = request.args.get('gender')
        if gender in ['male', 'female', 'other']:
            session['user_gender'] = gender
    # Steps 1-4
    if 1 <= step <= 4:
        return render_template(f"step{step}.html", current_step=step)
    # After step4, go to chat
    return redirect(url_for("chat"))

@app.route("/chat")
def chat():
    if not google.authorized:
        return redirect(url_for("login"))
<<<<<<< HEAD
    choice = session.get('avatar_choice', 'male')
    # Map choice to filename
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
        messages=[{"role":"system","content":"You are Dr. Erosi, professional yet playful sexual education AI."},
                  {"role":"user","content":user_msg}]
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
=======
    gender = session.get('user_gender', 'other')
    if gender == 'male':
        avatar_file = 'avatar_female.png'
    elif gender == 'female':
        avatar_file = 'avatar_male.png'
    else:
        avatar_file = 'avatar_andro.png'
    return render_template('chat.html', avatar_file=avatar_file)
>>>>>>> parent of d0d552f (Clean project skeleton and fix avatar selection)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
