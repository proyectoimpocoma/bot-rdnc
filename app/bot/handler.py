from pathlib import Path

from app.data import cargar_data, processor
from app.nlp import extractor_entity, normalizar_municipios
from app.nlp.extractor import add_rules
from app.services import consultar_ruta

PATH_FILE = Path("data/RNDC.xlsx")


class BotHandler:
    def __init__(self):
        df_raw = cargar_data(PATH_FILE)
        self.df = processor(df_raw)
        self.municipios = self.df["MUNICIPIOORIGEN"].unique().to_list()
        add_rules()

    def run(self, text: str):
        ruta = extractor_entity(text)
        origen = normalizar_municipios(ruta["origen"], self.municipios)
        destino = normalizar_municipios(ruta["destino"], self.municipios)
        return consultar_ruta(self.df, origen, destino)
