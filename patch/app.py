from flask import Flask, render_template, request, jsonify, redirect, url_for, session

@app.route("/")
def chat():
    # Obtenemos el avatar desde la sesión o por defecto 'male'
    avatar = session.get("avatar", "male")
    # Renderizamos el chat con los vídeos apropiados
    return render_template(
        "chat.html",
        avatar_video=f"{avatar}_loop.webm",
        avatar_speaking=f"{avatar}_loop.webm"
    )
