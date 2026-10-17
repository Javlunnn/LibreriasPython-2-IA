"""Punto de entrada principal del proyecto de Ejemplos de Librerías.

Por defecto abre la interfaz gráfica interactiva con las opciones de todos los ejemplos.
También soporta ejecución directa en terminal pasando el argumento --cli.

Uso:
    python main.py         # Abre la ventana gráfica con todas las opciones
    python main.py --cli   # Ejecuta todos los ejemplos secuencialmente en consola
"""
import io
import sys

# Si se ejecuta en modo ventana sin consola (PyInstaller --noconsole),
# sys.stdout y sys.stderr son None en Windows. Se redirigen a un buffer seguro.
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

# Importar explícitamente todos los módulos de ejemplo para que PyInstaller los incluya
import ejemplo_01_math
import ejemplo_02_random
import ejemplo_03_datetime
import ejemplo_04_csv
import ejemplo_05_fpdf
import ejemplo_06_reportlab
import ejemplo_07_numpy
import ejemplo_08_pandas
import ejemplo_09_matplotlib
import ejemplo_10_requests
import ejemplo_11_flask
import ejemplo_12_sklearn


def ejecutar_modo_consola():
    """Ejecuta todos los ejemplos uno tras otro en la consola."""
    print("Iniciando ejecución de todos los ejemplos en consola...\n")
    ejemplo_01_math.main()
    ejemplo_02_random.main()
    ejemplo_03_datetime.main()
    ejemplo_04_csv.main()
    ejemplo_05_fpdf.main()
    ejemplo_06_reportlab.main()
    ejemplo_07_numpy.main()
    ejemplo_08_pandas.main()
    ejemplo_09_matplotlib.main()
    ejemplo_10_requests.main()
    ejemplo_11_flask.demo_sin_servidor()
    ejemplo_12_sklearn.main()
    print("\nListo. Revisa la carpeta 'salida' para ver los archivos generados.")


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--cli", "--consola", "--console", "--terminal"):
        ejecutar_modo_consola()
    else:
        from gui import iniciar_interfaz
        iniciar_interfaz()


if __name__ == "__main__":
    main()
