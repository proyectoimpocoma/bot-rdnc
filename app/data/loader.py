from pathlib import Path

import polars as pl

from app.core import get_app_logger

logger = get_app_logger("loader")


def cargar_data(path: Path, skip_rows: int = 0) -> pl.DataFrame:
    """Carga los datos desde un archivo Excel en un DataFrame de Polars."""

    # Buena práctica: Validar que el archivo existe antes de intentar abrirlo
    if not path.exists():
        logger.error(f"El archivo no existe en la ruta: {path}")
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    try:
        logger.info(f"Leyendo archivo Excel desde: {path}")
        df = pl.read_excel(path)
        return df

    except PermissionError:
        logger.error(f"Error de permisos al intentar leer: {path}")
        raise  # 'raise' a secas preserva el traceback original de Python

    except Exception as e:
        logger.error(f"Error inesperado al leer el archivo {path}: {e!s}")
        raise  # Evitamos que la función retorne 'None' en caso de error
