"""Ejemplo 1: librería math (funciones matemáticas)."""
import math
from utilidades import titulo


def main():
    titulo("1. MATH")

    # Constantes
    print("pi =", math.pi)
    print("e  =", math.e)

    # Raíces, potencias y logaritmos
    print("Raíz cuadrada de 144:", math.sqrt(144))
    print("2 elevado a la 10:", math.pow(2, 10))
    print("Logaritmo natural de e:", math.log(math.e))
    print("Logaritmo base 10 de 1000:", math.log10(1000))

    # Redondeos
    print("ceil(4.2) =", math.ceil(4.2))
    print("floor(4.8) =", math.floor(4.8))

    # Trigonometría (los ángulos van en radianes)
    angulo = math.radians(30)
    print("seno de 30 grados:", round(math.sin(angulo), 4))
    print("coseno de 60 grados:", round(math.cos(math.radians(60)), 4))

    # Otras funciones útiles
    print("Factorial de 5:", math.factorial(5))
    print("MCD de 48 y 18:", math.gcd(48, 18))

    # Ejemplo práctico: área de un círculo
    radio = 7
    print(f"Área de un círculo de radio {radio}: {math.pi * radio ** 2:.2f}")


if __name__ == "__main__":
    main()
