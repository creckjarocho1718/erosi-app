from flask import Flask, render_template, request, jsonify, session
from gtts import gTTS
import uuid
import os

app = Flask(__name__)

@app.route("/")
def chat():
    avatar = session.get('avatar', 'male')
    return render_template("chat.html", avatar_video=f"{avatar}_loop.webm", avatar_speaking=f"{avatar}_loop.webm")

@app.route("/api/message", methods=["POST"])
def api_message():
    user_input = request.json.get("message")
    response_text = f"Erosi dice: {user_input}"  # Aquí iría tu lógica GPT o Rasa
    tts = gTTS(text=response_text, lang='es')
    filename = f"static/audio/response_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return jsonify({"text": response_text, "audio": "/" + filename})

if __name__ == "__main__":
    app.run(debug=True)
