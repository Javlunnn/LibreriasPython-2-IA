"""Ejemplo 12: librería scikit-learn (aprendizaje automático)."""
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from utilidades import titulo


def regresion_lineal():
    print("\n--- Regresión lineal ---")
    # Datos: horas de estudio -> calificación (con un poco de ruido)
    rng = np.random.default_rng(0)
    horas = rng.uniform(1, 10, size=(50, 1))
    notas = 4.5 + 0.5 * horas.ravel() + rng.normal(0, 0.3, 50)

    X_ent, X_prueba, y_ent, y_prueba = train_test_split(
        horas, notas, test_size=0.2, random_state=42
    )
    modelo = LinearRegression().fit(X_ent, y_ent)
    pred = modelo.predict(X_prueba)

    print(f"Pendiente: {modelo.coef_[0]:.3f} | Intercepto: {modelo.intercept_:.3f}")
    print(f"R2: {r2_score(y_prueba, pred):.3f}")
    print(f"Error cuadrático medio: {mean_squared_error(y_prueba, pred):.3f}")
    print(f"Predicción para 8 horas de estudio: {modelo.predict([[8]])[0]:.2f}")


def clasificacion():
    print("\n--- Clasificación con KNN (dataset Iris) ---")
    iris = load_iris()
    X_ent, X_prueba, y_ent, y_prueba = train_test_split(
        iris.data, iris.target, test_size=0.3, random_state=42
    )
    modelo = KNeighborsClassifier(n_neighbors=5).fit(X_ent, y_ent)
    pred = modelo.predict(X_prueba)
    print(f"Precisión (accuracy): {accuracy_score(y_prueba, pred):.3f}")

    flor = [[5.1, 3.5, 1.4, 0.2]]
    clase = modelo.predict(flor)[0]
    print("Una flor con medidas", flor[0], "es de la especie:", iris.target_names[clase])


def agrupamiento():
    print("\n--- Agrupamiento con KMeans ---")
    iris = load_iris()
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=42).fit(iris.data)
    print("Cantidad de elementos por grupo:", np.bincount(kmeans.labels_))


def main():
    titulo("12. SCIKIT-LEARN")
    regresion_lineal()
    clasificacion()
    agrupamiento()


if __name__ == "__main__":
    main()
