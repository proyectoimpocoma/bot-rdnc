import polars as pl

from app.core import get_app_logger

logger = get_app_logger("query_service")


def consultar_ruta(
    df: pl.DataFrame, origen: str | None, destino: str | None
) -> pl.DataFrame:
    """
    Filtra el DataFrame (que ya debe venir pre-procesado y agrupado)
    para una ruta específica.
    """
    if not origen or not destino:
        logger.warning("Falta el origen o el destino para realizar la consulta.")
        return pl.DataFrame()

    logger.info(f"Realizando consulta en la base de datos: {origen} -> {destino}")

    resultado = df.filter(
        (pl.col("MUNICIPIOORIGEN") == origen) & (pl.col("MUNICIPIODESTINO") == destino)
    ).sort("VALOR_PROMEDIO_UNITARIO")

    return resultado
