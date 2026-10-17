"""Ejemplo 7: librería NumPy (cálculo numérico con arreglos)."""
import numpy as np
from utilidades import titulo


def main():
    titulo("7. NUMPY")

    # Creación de arreglos
    a = np.array([1, 2, 3, 4, 5])
    print("Arreglo a:", a)
    print("Ceros 2x3:\n", np.zeros((2, 3)))
    print("Rango 0..9 paso 3:", np.arange(0, 10, 3))
    print("5 valores entre 0 y 1:", np.linspace(0, 1, 5))

    # Operaciones vectorizadas (sin bucles)
    print("a * 2 =", a * 2)
    print("a ** 2 =", a ** 2)
    print("a + a =", a + a)

    # Estadísticas
    datos = np.array([12, 15, 11, 20, 18, 25])
    print("\nMedia:", datos.mean())
    print("Mediana:", np.median(datos))
    print("Desviación estándar:", round(datos.std(), 3))
    print("Máximo / Mínimo:", datos.max(), "/", datos.min())

    # Matrices
    m1 = np.array([[1, 2], [3, 4]])
    m2 = np.array([[5, 6], [7, 8]])
    print("\nMultiplicación de matrices:\n", m1 @ m2)
    print("Transpuesta de m1:\n", m1.T)
    print("Determinante de m1:", round(np.linalg.det(m1), 2))

    # Indexación booleana
    print("\nElementos de 'datos' mayores a 15:", datos[datos > 15])

    # Números aleatorios con NumPy
    rng = np.random.default_rng(42)
    print("Matriz aleatoria 2x3:\n", rng.integers(1, 10, size=(2, 3)))

    # Cambiar la forma
    print("Reshape de 0..5 a 2x3:\n", np.arange(6).reshape(2, 3))


if __name__ == "__main__":
    main()
