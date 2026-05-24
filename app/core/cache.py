"""Módulo para gestionar el caché persistente del proyecto."""

from pathlib import Path

from diskcache import Cache

from app.core.logging import get_app_logger

logger = get_app_logger("cache")

# Definir la ruta de almacenamiento del caché persistente
CACHE_DIR = Path("data/sicetac_cache")

try:
    # Inicializar la caché persistente
    # diskcache crea el directorio automáticamente si no existe
    sicetac_cache = Cache(str(CACHE_DIR))
    logger.info(f"Caché persistente inicializado en: {CACHE_DIR.resolve()}")
except Exception as e:
    logger.error(f"Error al inicializar el caché persistente en {CACHE_DIR}: {e!s}")
    raise
