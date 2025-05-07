# Parche: actualizar función chat para definir avatar desde sesión
from flask import session

@app.route("/")
def chat():
    # Obtenemos el avatar desde la sesión o usamos 'male' por defecto
    avatar = session.get("avatar", "male")
    # Renderizamos el chat con los vídeos apropiados
    return render_template(
        "chat.html",
        avatar_video=f"{avatar}_loop.webm",
        avatar_speaking=f"{avatar}_loop.webm"
    )
