""" """

import asyncio
from pathlib import Path

import polars as pl

from app.core.logging import get_app_logger
from app.data import cargar_data, processor
from app.models.sicetac import SicetacParams
from app.nlp.normalizer import normalizar_municipios
from app.scrapper import playwright_sicetac
from app.services import consultar_ruta

PATH_FILE = Path("data/RNDC.xlsx")

logger = get_app_logger("bot_handler")


class BotHandler:
    def __init__(self):
        df_raw = cargar_data(PATH_FILE)
        self.df = processor(df_raw)
        self.origenes = self.df["MUNICIPIOORIGEN"].unique()
        self.destinos = self.df["MUNICIPIODESTINO"].unique()
        self.municipios = (
            pl.concat([self.origenes, self.destinos]).unique().unique().to_list()
        )

    def _run_scrapping(
        self,
        params: SicetacParams,
    ):
        logger.info(
            f"Ejecutando scrapping con: Origen='{params.origen}', Destino='{params.destino}', Configuración='{params.configuracion}', Condición de Carga='{params.condicion_carga}', Carrocería='{params.carroceria}', Tipo de Carga='{params.tipo_carga} ', Horas Cargue/Descargue='{params.horas_cargue_descargue}'"
        )
        try:
            return asyncio.run(playwright_sicetac(params))
        except Exception as e:
            logger.error(f"Error ejecutando playwright_sicetac: {e!s}")
            return False

    def run(
        self,
        params: SicetacParams,
    ) -> dict:
        logger.info(
            "Iniciando proceso de consulta de ruta con los siguientes parámetros:"
        )
        # Normalizar los nombres de origen y destino usando la lista combinada de municipios
        origen_df = normalizar_municipios(params.origen, self.municipios)
        destino_df = normalizar_municipios(params.destino, self.municipios)

        if not origen_df or not destino_df:
            raise ValueError(
                "No pude identificar las ciudades de origen y destino. "
                "Selecciona ambos campos antes de continuar."
            )

        costo = self._run_scrapping(params)

        return {
            "origen": params.origen,
            "destino": params.destino,
            "configuracion": params.configuracion,
            "costo_sicetac": costo,
            "ruta_db": consultar_ruta(
                self.df,
                origen=origen_df,
                destino=destino_df,
                configuracion=params.configuracion,
            ),
        }
