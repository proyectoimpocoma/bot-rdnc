import unicodedata

from rapidfuzz import fuzz, process

from app.core import get_app_logger

logger = get_app_logger("normalizer")


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.upper().strip()


def normalizar_municipios(
    nombre: str, lista: list[str], umbral: int = 80
) -> str | None:
    resultado, score, _ = process.extractOne(
        nombre.upper(), lista, scorer=fuzz.token_set_ratio
    )
    logger.info(f"Match: '{nombre}' - '{resultado}' (score: {score})  ")
    return resultado if score >= umbral else None
