
from flask import Flask, render_template, redirect
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

@app.route("/")
def index():
    return redirect("/chat")

@app.route("/chat")
def chat():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)
