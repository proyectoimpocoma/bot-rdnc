import polars as pl

from app.core.logging import get_app_logger

logger = get_app_logger("processor")


def processor(df: pl.DataFrame):
    logger.info(df.head())
    df = df.filter(
        ~pl.col("NATURALEZACARGA").is_in(["Carga Peligrosa", "Desechos Peligrosos"])
    )

    df = df.select(
        "COD_CONFIG_VEHICULO",
        "MUNICIPIOORIGEN",
        "MUNICIPIODESTINO",
        "VIAJESTOTALES",
        "VALORESPAGADOS",
    )

    df_grouped = (
        df.filter((pl.col("VALORESPAGADOS") > 0) & (pl.col("VIAJESTOTALES") > 0))
        .with_columns(
            (pl.col("VALORESPAGADOS") / pl.col("VIAJESTOTALES")).alias("VALOR_UNITARIO")
        )
        .group_by("COD_CONFIG_VEHICULO", "MUNICIPIOORIGEN", "MUNICIPIODESTINO")
        .agg(
            pl.col("VIAJESTOTALES").sum(),
            pl.col("VALORESPAGADOS").sum(),
            pl.col("VALOR_UNITARIO").mean().alias("VALOR_PROMEDIO_UNITARIO"),
        )
        .sort("VALOR_PROMEDIO_UNITARIO")
    )
    logger.info(df_grouped.head())

    return df_grouped
