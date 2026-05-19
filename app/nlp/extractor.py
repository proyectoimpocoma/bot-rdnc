from pathlib import Path

import spacy
from spacy import Language

from app.core import get_app_logger
from app.data import cargar_data

logger = get_app_logger("extractor")

# Cargamos el modelo en memoria una sola vez
nlp: Language | None = None
try:
    nlp = spacy.load("es_core_news_lg")
except OSError:
    logger.error(
        "No se encontró el modelo de spaCy. Ejecuta: uv run python -m spacy download es_core_news_lg"
    )
    nlp = None


def read_municipios():
    df = cargar_data(Path("data/municipios.xls"), skip_rows=5)
    lista = df["Nombre_Municipio"].to_list()
    lista_minusculas = [
        str(municipio).lower() for municipio in lista if municipio is not None
    ]
    return lista_minusculas


def add_rules():
    if nlp is None:
        raise RuntimeError(
            "No se encontró el modelo de spaCy. Ejecuta: uv run python -m spacy download es_core_news_lg"
        )
        logger.error(
            "No se encontró el modelo de spaCy. Ejecuta: uv run python -m spacy download es_core_news_lg"
        )

    # Validar que no hayamos agregado la regla antes
    if "entity_ruler" in nlp.pipe_names:
        return

    # 1. Crear el "Ruler" (Reglamento de entidades)
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    # 2. Supongamos que esta lista viene de tu DataFrame:
    # df["MUNICIPIOORIGEN"].unique().to_list()
    lista_municipios_excel = read_municipios()

    # 3. Crear los patrones para que spaCy los reconozca SÍ o SÍ
    patrones = []
    for municipio in lista_municipios_excel:
        patrones.append({"label": "LOC", "pattern": [{"LOWER": municipio}]})

    # 4. Inyectar las reglas a spaCy
    ruler.add_patterns(patrones)
    logger.info("Reglas de spaCy cargadas exitosamente con los datos del Excel")


def extractor_entity(text: str) -> dict:
    """
    Toma un texto libre y extrae las entidades que representan
    el municipio de origen y el municipio de destino.
    """
    if nlp is None:
        raise RuntimeError("El modelo de NLP no esta disponible")

    doc = nlp(text)

    logger.info(doc)

    # Opcional: Filtrar solo las entidades geográficas (LOC = Localización)
    ciudades = [ent.text for ent in doc.ents if ent.label_ in ("LOC", "GPE")]

    # ciudades = [entidad.text for entidad in doc.ents]

    origen = ciudades[0] if len(ciudades) > 0 else None
    destino = ciudades[1] if len(ciudades) > 1 else None

    logger.info(f"Entidades extraidas -> Origen: {origen}, Destinos: {destino}")

    return {"origen": origen, "destino": destino}
