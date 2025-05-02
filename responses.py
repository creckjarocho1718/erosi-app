# responses.py
def responder(message, perfil):
    msg = message.lower()
    if "hola" in msg:
        return "¡Hola! ¿Cómo puedo ayudarte hoy?"
    if "inseguro" in msg or "triste" in msg:
        return "Entiendo cómo te sientes. ¿Te gustaría que hablemos de técnicas para ganar confianza?"
    if "juguetes" in msg:
        return "Tengo varias recomendaciones según tus gustos. ¿Prefieres algo suave o un reto más atrevido?"
    return "Cuéntame más... estoy escuchando."
