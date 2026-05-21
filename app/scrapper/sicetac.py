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


async def export_sicetac_combinaciones(output_path: Path):
    """Exporta las combinaciones de origen y destino disponibles en SICETAC."""
    playwright, browser, context, page = await new_rndc_page()
    try:
        await page.goto(URL_SICETAC)
        await page.wait_for_selector(SELECTOR_ORIGEN_VIAJE)

        origenes = [
            text.strip()
            for text in await page.locator(
                f"{SELECTOR_ORIGEN_VIAJE} option"
            ).all_text_contents()
            if text.strip()
        ]

        combos = {}
        for origen in origenes:
            await page.locator(SELECTOR_ORIGEN_VIAJE).select_option(origen)
            await page.wait_for_timeout(500)  # esperar que el destino se actualice

            destinos = [
                text.strip()
                for text in await page.locator(
                    f"{SELECTOR_DESTINO_VIAJE} option"
                ).all_text_contents()
                if text.strip()
            ]
            combos[origen] = destinos

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(combos, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return combos
    except Exception as e:
        logger.error(f"Error exportando combinaciones SICETAC: {e!s}")


async def playwright_sicetac(
    origen: str,
    destino: str,
    configuracion: str,
    condicion_carga: str,
    Carroceria: str,
    tipo_carga: str,
) -> str | bool:
    """Función placeholder para el scrapper de SICETAC."""
    logger.info("playwright_sicetac aún no implementado.")

    # options_path = Path("data/sicetac_combinaciones.json")
    # if not options_path.exists():
    # await export_sicetac_combinaciones(options_path)

    playwright, browser, context, page = await new_rndc_page()
    try:
        await page.goto(URL_SICETAC)
        logger.info(f"Navegando a: {URL_SICETAC}")

        await page.locator(SELECTOR_ORIGEN_VIAJE).select_option(origen)
        await page.locator(SELECTOR_DESTINO_VIAJE).select_option(destino)

        await page.locator(SELECTOR_CONFIG_VEHICULO).select_option(configuracion)

        await page.locator(SELECTOR_CONDICION_CARGA).select_option(condicion_carga)
        await page.locator(SELECTOR_CARROCERIA_VEHICULO).select_option(Carroceria)
        await page.locator(SELECTOR_TIPO_CARGA).select_option(tipo_carga)

        await page.locator(SELECTOR_HORAS_CARGUE).fill("4")
        await page.locator(SELECTOR_HORAS_DESCARGUE).fill("4")

        capcha_text = await page.locator(SELECTOR_CAPTCHA).text_content()
        sum_captcha = sum_detected(str(capcha_text))

        await page.locator(SELECTOR_RESULTADO_CAPTCHA).fill(str(sum_captcha))
        await page.locator(SELECTOR_BT_CALCULAR).click()

        value = await page.locator(SELECTOR_COSTO_TOTAL_VIAJE).input_value()
        logger.info(f"Resultado del cálculo: {value}")

        return value
    except Exception as e:
        logger.error(f"Error en playwright_sicetac: {e!s}")
        return False
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()
        logger.info("Navegador cerrado en playwright_sicetac.")
