"""Ejemplo 3: librería datetime (fechas y horas)."""
from datetime import datetime, date, timedelta
from utilidades import titulo


def main():
    titulo("3. DATETIME")

    ahora = datetime.now()
    print("Fecha y hora actual:", ahora)
    print("Solo la fecha:", date.today())

    # Formatear con strftime
    print("Formato dd/mm/aaaa:", ahora.strftime("%d/%m/%Y"))
    print("Formato con hora:", ahora.strftime("%d/%m/%Y %H:%M:%S"))

    # Convertir texto a fecha con strptime
    nacimiento = datetime.strptime("15/03/2000", "%d/%m/%Y")
    print("Fecha leída del texto:", nacimiento.date())

    # Sumar y restar tiempo con timedelta
    en_30_dias = ahora + timedelta(days=30)
    print("Dentro de 30 días:", en_30_dias.strftime("%d/%m/%Y"))
    hace_una_semana = ahora - timedelta(weeks=1)
    print("Hace una semana:", hace_una_semana.strftime("%d/%m/%Y"))

    # Diferencia entre fechas
    diferencia = ahora - nacimiento
    print("Días transcurridos desde 15/03/2000:", diferencia.days)

    # Calcular edad aproximada
    edad = ahora.year - nacimiento.year - (
        (ahora.month, ahora.day) < (nacimiento.month, nacimiento.day)
    )
    print("Edad:", edad, "años")

    # Día de la semana (0 = lunes, 6 = domingo)
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    print("Hoy es:", dias[ahora.weekday()])


if __name__ == "__main__":
    main()
