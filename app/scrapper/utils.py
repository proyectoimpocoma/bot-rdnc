"Utilidades para el scrapper de RNDC."

from datetime import date
from app.core import get_app_logger
import re

logger = get_app_logger("utils")


def sum_detected(text: str) -> int:
    """Detecta y suma los números presentes en el texto dado.
    Args:
        text (str): El texto del cual se extraerán los números."""
    nums = re.findall(r"-?\d+", text)

    logger.info(f"Números detectados para el captcha: {nums}")

    return sum(int(n) for n in nums)


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
