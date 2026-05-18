from pathlib import Path

import polars as pl

from app.data import cargar_data, processor
from app.nlp import extractor_entity, normalizar_municipios
from app.nlp.extractor import add_rules
from app.services import consultar_ruta

PATH_FILE = Path("data/RNDC.xlsx")


class BotHandler:
    def __init__(self):
        df_raw = cargar_data(PATH_FILE)
        self.df = processor(df_raw)
        self.origenes = self.df["MUNICIPIOORIGEN"].unique()
        self.destinos = self.df["MUNICIPIODESTINO"].unique()
        self.municipios = pl.concat([self.origenes, self.destinos]).unique().to_list()
        add_rules()

    def run(self, text: str):
        ruta = extractor_entity(text)

        if not ruta["origen"] or not ruta["destino"]:
            raise ValueError(
                "No pude identificar las ciudades de origen y destino. "
                "Intenta con algo como: 'De Bogotá a Medellín'"
            )
        origen = normalizar_municipios(ruta["origen"], self.municipios)
        destino = normalizar_municipios(ruta["destino"], self.municipios)
        return consultar_ruta(self.df, origen, destino)
