import unicodedata

from rapidfuzz import fuzz, process, utils

from app.core import get_app_logger

logger = get_app_logger("normalizer")


def clean_text(text: str) -> str:
    """Quita tildes, signos diacríticos y convierte a mayúsculas."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower().strip()


def normalizar_municipios(
    nombre: str | None, lista: list[str], umbral: int = 80
) -> str | None:
    if not nombre or not lista:
        return None

    nombre_limpio = clean_text(nombre)

    lista_cortada = [
        municipio.split()[0] for municipio in lista if municipio is not None
    ]

    # --- INTENTO 1: Usando la lista recortada ---
    march_corto = process.extractOne(
        nombre_limpio,
        lista_cortada,
        scorer=fuzz.token_set_ratio,
        processor=utils.default_process,
    )

    if march_corto:
        _, score_corto, indice = march_corto
        if score_corto >= umbral:
            resultado_final = lista[indice]
            logger.info(
                f"✅ ACEPTADO (Corto): '{nombre}' -> '{resultado_final}' (Score: {score_corto:.1f})"
            )
            return resultado_final

    # --- INTENTO 2: Si falló, intentar con la lista completa ---
    match_completo = process.extractOne(
        nombre_limpio,
        lista,
        scorer=fuzz.token_set_ratio,
        processor=utils.default_process,
    )

    if match_completo:
        resultado_completo, score_completo, _ = match_completo
        if score_completo >= umbral:
            logger.info(
                f"✅ ACEPTADO (Completo): '{nombre}' -> '{resultado_completo}' (Score: {score_completo:.1f})"
            )
            return resultado_completo

    # --- RECHAZADO: Si ninguno superó el umbral ---
    # Logeamos el que sacó mejor puntaje para saber qué falló
    if match_completo:
        mejor_res, mejor_score, _ = match_completo
        logger.warning(
            f"❌ RECHAZADO: '{nombre}' -> '{mejor_res}' (Mejor Score: {mejor_score:.1f} < {umbral})"
        )
    return None
