"""Ejemplo 10: librería Requests (peticiones HTTP).

Usa la API pública gratuita https://jsonplaceholder.typicode.com
Necesita conexión a Internet. Si no hay, el programa lo avisa sin fallar.
"""
import requests
from utilidades import titulo

URL = "https://jsonplaceholder.typicode.com"


def main():
    titulo("10. REQUESTS")

    try:
        # GET: obtener un recurso
        r = requests.get(f"{URL}/posts/1", timeout=10)
        print("Código de estado GET:", r.status_code)
        post = r.json()
        print("Título del post:", post["title"])

        # GET con parámetros en la URL (?userId=1)
        r = requests.get(f"{URL}/posts", params={"userId": 1}, timeout=10)
        print("Posts del usuario 1:", len(r.json()))

        # POST: enviar datos
        nuevo = {"title": "Mi post", "body": "Contenido de prueba", "userId": 1}
        r = requests.post(f"{URL}/posts", json=nuevo, timeout=10)
        print("Código de estado POST:", r.status_code)
        print("Respuesta del servidor:", r.json())

        # Manejo de errores HTTP (404)
        r = requests.get(f"{URL}/posts/99999", timeout=10)
        print("Recurso inexistente, código:", r.status_code)
        r.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print("Error HTTP controlado:", e)
    except requests.exceptions.RequestException as e:
        print("No se pudo conectar (revisa tu Internet):", type(e).__name__)


if __name__ == "__main__":
    main()
