"""Ejemplo 4: librería csv (leer y escribir archivos CSV)."""
import csv
from utilidades import titulo, ruta_salida


def main():
    titulo("4. CSV")
    archivo = ruta_salida("alumnos.csv")

    # --- Escritura con csv.writer ---
    filas = [
        ["nombre", "edad", "calificacion"],
        ["Ana", 20, 9.5],
        ["Luis", 22, 8.0],
        ["Marta", 21, 9.0],
    ]
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerows(filas)
    print("Archivo creado:", archivo.name)

    # --- Lectura con csv.reader ---
    print("\nLectura con csv.reader:")
    with open(archivo, newline="", encoding="utf-8") as f:
        for fila in csv.reader(f):
            print(fila)

    # --- Lectura con DictReader (cada fila es un diccionario) ---
    print("\nLectura con csv.DictReader:")
    with open(archivo, newline="", encoding="utf-8") as f:
        alumnos = list(csv.DictReader(f))
    for a in alumnos:
        print(f"{a['nombre']} tiene {a['edad']} años y calificación {a['calificacion']}")

    promedio = sum(float(a["calificacion"]) for a in alumnos) / len(alumnos)
    print(f"Promedio del grupo: {promedio:.2f}")

    # --- Escritura con DictWriter ---
    archivo2 = ruta_salida("alumnos_aprobados.csv")
    aprobados = [a for a in alumnos if float(a["calificacion"]) >= 9]
    with open(archivo2, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["nombre", "edad", "calificacion"])
        escritor.writeheader()
        escritor.writerows(aprobados)
    print("Archivo creado:", archivo2.name)


if __name__ == "__main__":
    main()
