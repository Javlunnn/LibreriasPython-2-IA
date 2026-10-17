import sys
from pathlib import Path

# Si se ejecuta como ejecutable compilado (PyInstaller), la ruta base es la del .exe
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

CARPETA_SALIDA = BASE_DIR / "salida"
CARPETA_SALIDA.mkdir(exist_ok=True)


def ruta_salida(nombre_archivo: str) -> Path:
    """Devuelve la ruta dentro de la carpeta 'salida' para guardar archivos."""
    return CARPETA_SALIDA / nombre_archivo


def titulo(texto: str) -> None:
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)
