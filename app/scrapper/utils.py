"Utilidades para el scrapper de RNDC."

from datetime import date


def sum_detected(text: str) -> int:
    """Detecta y suma los números presentes en el texto dado.
    Args:
        text (str): El texto del cual se extraerán los números."""
    numbers = [int(s) for s in text.split() if s.isdigit()]

    return sum(numbers)


def previous_month_year(today: date | None = None) -> str:
    """Calcula el año y mes anterior al mes actual en formato 'AAAAMM'."""
    today = today or date.today()
    # Si el mes actual es enero, el mes anterior es diciembre del año anterior
    if today.month == 1:
        year = today.year - 1
        month = 12
    else:
        year = today.year
        month = today.month - 1
    return f"{year:04d}{month:02d}"
