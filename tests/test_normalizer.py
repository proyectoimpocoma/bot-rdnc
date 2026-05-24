from app.nlp.normalizer import normalizar_sicetac_a_rndc
from app.nlp.parser import parse_rndc, parse_sicetac


def test_parse_sicetac_formats():
    # Tipo A (3 parts)
    res_a = parse_sicetac("AEROPUERTO - RIONEGRO - ANTIOQUIA")
    assert res_a["lugar"] == "AEROPUERTO"
    assert res_a["municipio"] == "RIONEGRO"
    assert res_a["departamento"] == "ANTIOQUIA"

    # Tipo B (2 parts, guión regular)
    res_b1 = parse_sicetac("AGUACHICA-CESAR")
    assert res_b1["lugar"] == "AGUACHICA"
    assert res_b1["municipio"] == "AGUACHICA"
    assert res_b1["departamento"] == "CESAR"

    # Tipo B (2 parts, guión con espacios)
    res_b2 = parse_sicetac("ARBOLETES - ANTIOQUIA")
    assert res_b2["lugar"] == "ARBOLETES"
    assert res_b2["municipio"] == "ARBOLETES"
    assert res_b2["departamento"] == "ANTIOQUIA"

    # Tipo C (1 part)
    res_c = parse_sicetac("BOGOTÁ")
    assert res_c["lugar"] == "BOGOTÁ"
    assert res_c["municipio"] == "BOGOTÁ"
    assert res_c["departamento"] == ""

    # Caso trampa (4 parts)
    res_trampa = parse_sicetac("BUENOS AIRES - LAS PAVAS - CANALETE - CORDOBA")
    assert res_trampa["lugar"] == "BUENOS AIRES - LAS PAVAS"
    assert res_trampa["municipio"] == "CANALETE"
    assert res_trampa["departamento"] == "CORDOBA"

    # Caso especial con en-dash (guión Unicode largo)
    res_unicode = parse_sicetac("ADJUNTAS - AGUACHICA – CESAR")  # noqa: RUF001
    assert res_unicode["lugar"] == "ADJUNTAS"
    assert res_unicode["municipio"] == "AGUACHICA"
    assert res_unicode["departamento"] == "CESAR"


def test_parse_rndc():
    # Caso simple
    res_simple = parse_rndc("ABEJORRAL ANTIOQUIA")
    assert res_simple["municipio"] == "ABEJORRAL"
    assert res_simple["departamento"] == "ANTIOQUIA"

    # Caso departamento multi-palabra (Valle del Cauca)
    res_multi = parse_rndc("CALI VALLE DEL CAUCA")
    assert res_multi["municipio"] == "CALI"
    assert res_multi["departamento"] == "VALLE DEL CAUCA"

    # Caso con barrio/lugar
    res_lugar = parse_rndc("AEROPUERTO RIONEGRO ANTIOQUIA")
    assert res_lugar["municipio"] == "AEROPUERTO RIONEGRO"
    assert res_lugar["departamento"] == "ANTIOQUIA"


def test_normalizar_sicetac_a_rndc():
    # Preparar datos de prueba
    lista_rndc = [
        "ABEJORRAL ANTIOQUIA",
        "RIONEGRO ANTIOQUIA",
        "AGUACHICA CESAR",
        "BOGOTA BOGOTA D. C.",
        "CALI VALLE DEL CAUCA",
    ]

    mock_lookup = {
        "AEROPUERTO - RIONEGRO - ANTIOQUIA": "RIONEGRO ANTIOQUIA",
        "AGUACHICA-CESAR": "AGUACHICA CESAR",
    }

    # 1. Probar HIT directo en lookup table
    res_hit = normalizar_sicetac_a_rndc("AEROPUERTO - RIONEGRO - ANTIOQUIA", lista_rndc, mock_lookup)
    assert res_hit == "RIONEGRO ANTIOQUIA"

    # 2. Probar MISS con fallback fuzzy exitoso (anclado por departamento)
    # "AGUADAS-CALDAS" no está en mock_lookup, pero sí queremos que lo resuelva fuzzy si estuviera en lista_rndc.
    # Vamos a añadir "AGUADAS CALDAS" a la lista y probar que resuelva
    lista_rndc_completa = [*lista_rndc, "AGUADAS CALDAS"]
    res_miss_fallback = normalizar_sicetac_a_rndc("AGUADAS-CALDAS", lista_rndc_completa, mock_lookup)
    assert res_miss_fallback == "AGUADAS CALDAS"
    # Debe haberse guardado en el lookup (cache-aside)
    assert "AGUADAS-CALDAS" in mock_lookup
    assert mock_lookup["AGUADAS-CALDAS"] == "AGUADAS CALDAS"

    # 3. Probar MISS con entrada sin departamento ("BOGOTÁ")
    res_no_dpto = normalizar_sicetac_a_rndc("BOGOTÁ", lista_rndc, mock_lookup)
    assert res_no_dpto == "BOGOTA BOGOTA D. C."
    assert "BOGOTÁ" in mock_lookup
