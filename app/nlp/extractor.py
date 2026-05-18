import spacy

from app.core import get_app_logger

logger = get_app_logger("extractor")

# Cargamos el modelo en memoria una sola vez
try:
    nlp = spacy.load("es_core_news_lg")
except OSError:
    logger.error(
        "No se encontró el modelo de spaCy. Ejecuta: uv run python -m spacy download es_core_news_lg"
    )
    nlp = None


def extractor_entity(text: str) -> dict:
    """
    Toma un texto libre y extrae las entidades que representan
    el municipio de origen y el municipio de destino.
    """
    if nlp is None:
        raise RuntimeError("El modelo de NLP no esta disponible")

    doc = nlp(text)

    # Opcional: Filtrar solo las entidades geográficas (LOC = Localización)
    # ubicaciones = [ent.text for ent in doc.ents if ent.label_ in ("LOC", "GPE")]

    ciudades = [entidad.text for entidad in doc.ents]

    origen = ciudades[0] if len(ciudades) > 0 else None
    destino = ciudades[1] if len(ciudades) > 1 else None

    logger.info(f"Entidades extraidas -> Origen: {origen}, Destinos: {destino}")

    return {"origen": origen, "destino": destino}
