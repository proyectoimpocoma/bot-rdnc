from pydantic import BaseModel


class SicetacParams(BaseModel):
    origen: str
    destino: str
    configuracion: str
    condicion_carga: str
    carroceria: str
    tipo_carga: str
    horas_cargue_descargue: str
