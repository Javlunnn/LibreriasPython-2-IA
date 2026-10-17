"""Ejemplo 2: librería random (números y elecciones aleatorias)."""
import random
from utilidades import titulo


def main():
    titulo("2. RANDOM")

    # Semilla: hace que los resultados sean repetibles
    random.seed(42)

    print("Entero entre 1 y 10:", random.randint(1, 10))
    print("Decimal entre 0 y 1:", round(random.random(), 4))
    print("Decimal entre 5 y 10:", round(random.uniform(5, 10), 4))

    frutas = ["manzana", "pera", "uva", "mango", "fresa"]
    print("Elección de una fruta:", random.choice(frutas))
    print("3 frutas distintas:", random.sample(frutas, 3))

    # Mezclar una lista (modifica la lista original)
    numeros = [1, 2, 3, 4, 5]
    random.shuffle(numeros)
    print("Lista mezclada:", numeros)

    # Simular el lanzamiento de un dado 10 veces
    tiradas = [random.randint(1, 6) for _ in range(10)]
    print("10 tiradas de dado:", tiradas)

    # Contraseña aleatoria sencilla
    caracteres = "abcdefghijklmnopqrstuvwxyz0123456789"
    clave = "".join(random.choice(caracteres) for _ in range(8))
    print("Clave aleatoria:", clave)


if __name__ == "__main__":
    main()
