--- app.py (antes)
-from flask import Flask, render_template, request, jsonify, redirect, url_for
+from flask import Flask, render_template, request, jsonify, redirect, url_for, session

 app = Flask(__name__)
 # … tu configuración de OAuth, rutas de login, etc.

-@app.route("/")
-def chat():
-    return render_template("chat.html",
-                           avatar_video="avatar_male_loop.webm",
-                           avatar_speaking=avatar + "_loop.webm")
+@app.route("/")
+def chat():
+    # Obtenemos el avatar desde la sesión o usamos 'male' por defecto
+    avatar = session.get("avatar", "male")
+    return render_template(
+        "chat.html",
+        avatar_video=f"{avatar}_loop.webm",
+        avatar_speaking=f"{avatar}_loop.webm"
+    )

 # … resto de tu código
