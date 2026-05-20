"""Módulo para scrapping de SICETAC utilizando Playwright."""

import json
from pathlib import Path

from app.core import get_app_logger
from app.scrapper.browser import new_rndc_page
from app.scrapper.selectors import (
    SELECTOR_BT_CALCULAR,
    SELECTOR_CAPTCHA,
    SELECTOR_CARROCERIA_VEHICULO,
    SELECTOR_CONDICION_CARGA,
    SELECTOR_CONFIG_VEHICULO,
    SELECTOR_COSTO_TOTAL_VIAJE,
    SELECTOR_DESTINO_VIAJE,
    SELECTOR_HORAS_CARGUE,
    SELECTOR_HORAS_DESCARGUE,
    SELECTOR_ORIGEN_VIAJE,
    SELECTOR_RESULTADO_CAPTCHA,
    SELECTOR_TIPO_CARGA,
    URL_SICETAC,
)
from app.scrapper.utils import sum_detected

logger = get_app_logger("main")


async def export_sicetac_data(output_path: Path):
    """Exporta las opciones de SICETAC a JSON."""
    playwright, browser, context, page = await new_rndc_page()
    try:
        await page.goto(URL_SICETAC)

        origen_options = [
            text.strip()
            for text in await page.locator(
                f"{SELECTOR_ORIGEN_VIAJE} option"
            ).all_text_contents()
            if text.strip()
        ]
        destino_options = [
            text.strip()
            for text in await page.locator(
                f"{SELECTOR_DESTINO_VIAJE} option"
            ).all_text_contents()
            if text.strip()
        ]
        payload = {"origen": origen_options, "destino": destino_options}

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return payload

    finally:
        await context.close()
        await browser.close()
        await playwright.stop()


async def playwright_sicetac(origen: str, destino: str):
    """Función placeholder para el scrapper de SICETAC."""
    logger.info("playwright_sicetac aún no implementado.")
    playwright, browser, context, page = await new_rndc_page()
    try:
        await page.goto(URL_SICETAC)
        logger.info(f"Navegando a: {URL_SICETAC}")

        await page.locator(SELECTOR_CONFIG_VEHICULO).select_option(
            "Tractocamión tres ejes con semiremolque de tres ejes"
        )

        await page.locator(SELECTOR_CONDICION_CARGA).select_option("CARGADO")
        await page.locator(SELECTOR_CARROCERIA_VEHICULO).select_option("ESTACAS")
        await page.locator(SELECTOR_TIPO_CARGA).select_option("General")

        options_path = Path("data/sicetac_options.json")
        if not options_path.exists():
            await export_sicetac_data(options_path)

        await page.locator(SELECTOR_ORIGEN_VIAJE).select_option(origen)
        await page.locator(SELECTOR_DESTINO_VIAJE).select_option(destino)

        await page.locator(SELECTOR_HORAS_CARGUE).fill("4")
        await page.locator(SELECTOR_HORAS_DESCARGUE).fill("4")

        capcha_text = await page.locator(SELECTOR_CAPTCHA).text_content()
        sum_captcha = sum_detected(str(capcha_text))

        await page.locator(SELECTOR_RESULTADO_CAPTCHA).fill(str(sum_captcha))
        await page.locator(SELECTOR_BT_CALCULAR).click()

        value = await page.locator(SELECTOR_COSTO_TOTAL_VIAJE).input_value()
        logger.info(f"Resultado del cálculo: {value}")
        await page.wait_for_timeout(9000)

        return value
    except Exception as e:
        logger.error(f"Error en playwright_sicetac: {e!s}")
        return False
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()
        logger.info("Navegador cerrado en playwright_sicetac.")
