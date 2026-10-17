"""Ejemplo 11: librería Flask (aplicación web / API).

Para levantar el servidor:   python ejemplo_11_flask.py
Luego abre en el navegador:  http://127.0.0.1:5000
"""
from flask import Flask, jsonify, request
from utilidades import titulo

app = Flask(__name__)

# "Base de datos" en memoria, solo para el ejemplo
tareas = [
    {"id": 1, "texto": "Aprender Flask", "hecha": False},
    {"id": 2, "texto": "Hacer un README", "hecha": True},
]


@app.route("/")
def inicio():
    return "<h1>Hola desde Flask</h1><p>Prueba <a href='/api/tareas'>/api/tareas</a></p>"


@app.route("/saludo/<nombre>")
def saludo(nombre):
    return f"¡Hola, {nombre}!"


@app.route("/api/tareas", methods=["GET"])
def listar_tareas():
    return jsonify(tareas)


@app.route("/api/tareas", methods=["POST"])
def crear_tarea():
    datos = request.get_json()
    if not datos or "texto" not in datos:
        return jsonify({"error": "Falta el campo 'texto'"}), 400
    nueva = {"id": len(tareas) + 1, "texto": datos["texto"], "hecha": False}
    tareas.append(nueva)
    return jsonify(nueva), 201


@app.route("/api/tareas/<int:tarea_id>", methods=["GET"])
def obtener_tarea(tarea_id):
    for t in tareas:
        if t["id"] == tarea_id:
            return jsonify(t)
    return jsonify({"error": "Tarea no encontrada"}), 404


def demo_sin_servidor():
    """Prueba las rutas con el cliente de pruebas de Flask (sin abrir puertos)."""
    titulo("11. FLASK (demo con test_client)")
    cliente = app.test_client()

    r = cliente.get("/saludo/Jav")
    print("GET /saludo/Jav ->", r.status_code, r.get_data(as_text=True))

    r = cliente.get("/api/tareas")
    print("GET /api/tareas ->", r.status_code, r.get_json())

    r = cliente.post("/api/tareas", json={"texto": "Probar POST"})
    print("POST /api/tareas ->", r.status_code, r.get_json())

    r = cliente.get("/api/tareas/99")
    print("GET /api/tareas/99 ->", r.status_code, r.get_json())


if __name__ == "__main__":
    # Ejecutado directamente: levanta el servidor real
    app.run(debug=True)
