"""Ejemplo 9: librería Matplotlib (gráficas)."""
import matplotlib
matplotlib.use("Agg")  # backend sin ventana: guarda las imágenes en archivos
import matplotlib.pyplot as plt
import numpy as np
from utilidades import titulo, ruta_salida


def main():
    titulo("9. MATPLOTLIB")

    # Una figura con 4 gráficas distintas
    fig, ejes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle("Ejemplos de gráficas con Matplotlib", fontsize=14)

    # 1) Gráfica de líneas
    x = np.linspace(0, 2 * np.pi, 100)
    ejes[0, 0].plot(x, np.sin(x), label="seno", color="blue")
    ejes[0, 0].plot(x, np.cos(x), label="coseno", color="red", linestyle="--")
    ejes[0, 0].set_title("Líneas")
    ejes[0, 0].legend()
    ejes[0, 0].grid(True)

    # 2) Gráfica de barras
    meses = ["Ene", "Feb", "Mar", "Abr"]
    ventas = [120, 150, 90, 180]
    ejes[0, 1].bar(meses, ventas, color="green")
    ejes[0, 1].set_title("Barras")
    ejes[0, 1].set_ylabel("Ventas")

    # 3) Gráfica de dispersión
    rng = np.random.default_rng(1)
    px, py = rng.random(50), rng.random(50)
    ejes[1, 0].scatter(px, py, c=py, cmap="viridis")
    ejes[1, 0].set_title("Dispersión")

    # 4) Gráfica de pastel
    ejes[1, 1].pie([40, 30, 20, 10], labels=["A", "B", "C", "D"], autopct="%1.1f%%")
    ejes[1, 1].set_title("Pastel")

    plt.tight_layout()
    salida = ruta_salida("graficas_matplotlib.png")
    plt.savefig(salida, dpi=100)
    plt.close()
    print("Imagen guardada:", salida.name)

    # Histograma aparte
    datos = rng.normal(loc=50, scale=10, size=500)
    plt.figure(figsize=(6, 4))
    plt.hist(datos, bins=20, color="orange", edgecolor="black")
    plt.title("Histograma de datos normales")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    salida2 = ruta_salida("histograma_matplotlib.png")
    plt.savefig(salida2, dpi=100)
    plt.close()
    print("Imagen guardada:", salida2.name)


if __name__ == "__main__":
    main()
