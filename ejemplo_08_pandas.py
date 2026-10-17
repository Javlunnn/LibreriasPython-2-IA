"""Ejemplo 8: librería Pandas (análisis de datos con tablas)."""
import pandas as pd
from utilidades import titulo, ruta_salida


def main():
    titulo("8. PANDAS")

    # Crear un DataFrame desde un diccionario
    df = pd.DataFrame({
        "nombre": ["Ana", "Luis", "Marta", "Pedro", "Sofía", "Diego"],
        "departamento": ["Ventas", "TI", "Ventas", "TI", "RH", "RH"],
        "salario": [15000, 22000, 16500, 25000, 14000, 14500],
        "antiguedad": [2, 5, 3, 8, 1, 2],
    })
    print("DataFrame completo:\n", df)

    print("\nPrimeras 3 filas:\n", df.head(3))
    print("\nInformación estadística:\n", df.describe())

    # Selección y filtrado
    print("\nSolo la columna salario:\n", df["salario"].head(3))
    print("\nEmpleados con salario > 15000:\n", df[df["salario"] > 15000])

    # Nueva columna calculada
    df["salario_anual"] = df["salario"] * 12
    print("\nCon columna de salario anual:\n", df[["nombre", "salario_anual"]])

    # Agrupación
    print("\nSalario promedio por departamento:")
    print(df.groupby("departamento")["salario"].mean())

    # Ordenar
    print("\nOrdenado por salario descendente:\n",
          df.sort_values("salario", ascending=False).head(3))

    # Guardar y leer CSV
    archivo = ruta_salida("empleados_pandas.csv")
    df.to_csv(archivo, index=False)
    leido = pd.read_csv(archivo)
    print("\nCSV guardado y leído de nuevo, filas:", len(leido))


if __name__ == "__main__":
    main()
