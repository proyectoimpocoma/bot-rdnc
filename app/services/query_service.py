import polars as pl

from app.core import get_app_logger
from rapidfuzz import fuzz, process, utils

logger = get_app_logger("query_service")


def fuzzy_match_best(
    query: str,
    candidates: list[str],
    threshold: int = 80,
    scorer=fuzz.token_set_ratio,
) -> tuple[str, float, int] | None:
    """Busca el mejor match fuzzy de un query dentro de una lista de candidatos."""
    match = process.extractOne(
        query,
        candidates,
        scorer=scorer,
        processor=utils.default_process,
    )
    if match and match[1] >= threshold:
        return match
    return None


def consultar_ruta(
    df: pl.DataFrame, origen: str | None, destino: str | None, configuracion: str | None
) -> pl.DataFrame:
    """
    Filtra el DataFrame (que ya debe venir pre-procesado y agrupado)
    para una ruta específica.
    """
    if not origen or not destino:
        logger.warning(
            "No se encontró una coincidencia exacta para el origen o el destino."
        )
        return pl.DataFrame()

    logger.info(
        f"Realizando consulta en la base de datos: {origen} -> {destino} (Configuración: {configuracion})"
    )

    resultado = df.filter(
        (pl.col("MUNICIPIOORIGEN") == origen)
        & (pl.col("MUNICIPIODESTINO") == destino)
        & (pl.col("COD_CONFIG_VEHICULO") == configuracion)
    )

    return resultado
