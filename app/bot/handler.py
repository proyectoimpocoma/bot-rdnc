import asyncio
from pathlib import Path

from spacy.util import logger

from app.data import cargar_data, processor
from app.nlp import extractor_entity, normalizar_municipios
from app.nlp.extractor import add_rules, read_municipios
from app.scrapper import playwright_sicetac
from app.services import consultar_ruta

PATH_FILE = Path("data/RNDC.xlsx")


class BotHandler:
    def __init__(self):
        df_raw = cargar_data(PATH_FILE)
        self.df = processor(df_raw)
        self.origenes = self.df["MUNICIPIOORIGEN"].unique()
        self.destinos = self.df["MUNICIPIODESTINO"].unique()
        self.municipios = read_municipios()
        add_rules()

    def run_scrapping(self, origen: str, destino: str):
        try:
            asyncio.run(playwright_sicetac(origen, destino))
        except Exception as e:
            logger.error(f"Error ejecutando playwright_sicetac: {e!s}")

    def run(self, text: str):
        ruta = extractor_entity(text)

        if not ruta["origen"] or not ruta["destino"]:
            raise ValueError(
                "No pude identificar las ciudades de origen y destino. "
                "Intenta con algo como: 'De Bogotá a Medellín'"
            )

        origen = normalizar_municipios(ruta["origen"], self.municipios)
        destino = normalizar_municipios(ruta["destino"], self.municipios)

        if not origen or not destino:
            raise ValueError(
                "No pude normalizar la ciudad de origen o destino. "
                "Verifica la ortografía o usa el nombre completo del municipio."
            )

        costo = asyncio.run(playwright_sicetac(origen, destino))
        return {
            "origen": origen,
            "destino": destino,
            "costo_sicetac": costo,
            "ruta_db": consultar_ruta(self.df, origen, destino),
        }
