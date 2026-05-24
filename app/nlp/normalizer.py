from rapidfuzz import fuzz, process, utils

from app.core import get_app_logger
from app.nlp.parser import clean_text, parse_rndc, parse_sicetac

logger = get_app_logger("normalizer")


def fuzzy_match_best(
    query: str,
    candidates: list[str],
    threshold: int = 80,
    scorer=fuzz.token_set_ratio,
) -> tuple[str, float, int] | None:
    """Busca el mejor match fuzzy de un query dentro de una lista de candidatos."""
    match = process.extractOne(
        query,
        candidates,
        scorer=scorer,
        processor=utils.default_process,
    )
    if match and match[1] >= threshold:
        return match
    return None


def normalizar_municipios(
    nombre: str | None, lista: list[str], umbral: int = 80
) -> str | None:
    """
    Función de normalización heredada. Preservada para compatibilidad.
    """
    if not nombre or not lista:
        return None

    nombre_limpio = clean_text(nombre)

    lista_cortada = [
        municipio.split()[0] for municipio in lista if municipio is not None
    ]

    # --- INTENTO 1: Usando la lista recortada ---
    match_corto = fuzzy_match_best(nombre_limpio, lista_cortada, threshold=umbral)
    if match_corto:
        _, score_corto, indice = match_corto
        resultado_final = lista[indice]
        logger.info(
            f"✅ ACEPTADO (Corto): '{nombre}' -> '{resultado_final}' (Score: {score_corto:.1f})"
        )
        return resultado_final

    # --- INTENTO 2: Si falló, intentar con la lista completa ---
    match_completo = fuzzy_match_best(nombre_limpio, lista, threshold=umbral)
    if match_completo:
        resultado_completo, score_completo, _ = match_completo
        logger.info(
            f"✅ ACEPTADO (Completo): '{nombre}' -> '{resultado_completo}' (Score: {score_completo:.1f})"
        )
        return resultado_completo

    # --- RECHAZADO: Si ninguno superó el umbral ---
    match_completo = process.extractOne(
        nombre_limpio,
        lista,
        scorer=fuzz.token_set_ratio,
        processor=utils.default_process,
    )
    if match_completo:
        mejor_res, mejor_score, _ = match_completo
        logger.warning(
            f"❌ RECHAZADO: '{nombre}' -> '{mejor_res}' (Mejor Score: {mejor_score:.1f} < {umbral})"
        )
    return None


def normalizar_sicetac_a_rndc(
    entrada_sicetac: str | None,
    lista_rndc: list[str],
    lookup: dict[str, str],
    umbral: int = 80,
) -> str | None:
    """
    Normaliza una entrada de SICETAC (Tipo A, B o C) a un valor de RNDC.

    1. Busca en O(1) en el lookup table cargado.
    2. Si falla, realiza fallback fuzzy anclado por el departamento de la entrada.
    3. Si el fallback tiene éxito, lo guarda en el lookup para consultas futuras (cache-aside).
    """
    if not entrada_sicetac or not lista_rndc:
        return None

    # 1. HIT en lookup table
    if entrada_sicetac in lookup:
        logger.info(
            f"🎯 HIT lookup table: '{entrada_sicetac}' -> '{lookup[entrada_sicetac]}'"
        )
        return lookup[entrada_sicetac]

    # 2. MISS - Aplicar fallback estructurado por departamento
    logger.info(
        f"🔍 MISS lookup table para: '{entrada_sicetac}'. Aplicando fallback por dpto..."
    )

    parsed_sic = parse_sicetac(entrada_sicetac)
    muni_clean = clean_text(parsed_sic["municipio"])
    dpto_clean = clean_text(parsed_sic["departamento"])
    lugar_clean = clean_text(parsed_sic["lugar"])

    # Filtrar candidatos de RNDC por departamento
    candidates = []
    for cand in lista_rndc:
        if cand is None:
            continue
        parsed_cand = parse_rndc(cand)
        cand_dpto_clean = clean_text(parsed_cand["departamento"])

        if dpto_clean:
            # Si hay dpto en la entrada, anclar por él
            if cand_dpto_clean == dpto_clean:
                candidates.append((cand, clean_text(parsed_cand["municipio"])))
        else:
            candidates.append((cand, clean_text(parsed_cand["municipio"])))

    # Si se filtró por dpto y no hay candidatos, remover el ancla de dpto como fallback
    if dpto_clean and not candidates:
        candidates = [
            (cand, clean_text(parse_rndc(cand)["municipio"]))
            for cand in lista_rndc
            if cand is not None
        ]

    # Realizar fuzzy matching
    best_cand = None
    best_score = -1.0

    for cand_full, cand_muni_clean in candidates:
        score_muni = fuzz.ratio(muni_clean, cand_muni_clean)

        if lugar_clean and lugar_clean != muni_clean:
            full_sic_clean = clean_text(
                parsed_sic["lugar"] + " " + parsed_sic["municipio"]
            )
            score_full = fuzz.ratio(full_sic_clean, cand_muni_clean)
        else:
            score_full = score_muni

        score = max(score_muni, score_full)

        if score > best_score:
            best_score = score
            best_cand = cand_full

    # Si supera el umbral, retornar y almacenar en lookup (cache-aside)
    if best_cand and best_score >= umbral:
        logger.info(
            f"✅ Fallback ACEPTADO: '{entrada_sicetac}' -> '{best_cand}' (Score: {best_score:.1f})"
        )
        lookup[entrada_sicetac] = best_cand
        return best_cand

    logger.warning(f"❌ Fallback RECHAZADO para: '{entrada_sicetac}'")
    return None
