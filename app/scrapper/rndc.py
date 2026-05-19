"""Scraper para descargar datos estadísticos de RNDC."""

from app.core.logging import get_app_logger
from app.scrapper.browser import new_rndc_page
from app.scrapper.selectors import (
    URL,
    SELECTOR_CAPTCHA,
    SELECTOR_RESULTADO,
    SELECTOR_FECHA_INICIAL,
    SELECTOR_BT_ESTADISTICAS,
)
from app.scrapper.utils import sum_detected, previous_month_year

logger = get_app_logger("rndc")


def playwright_rndc():
    """Descarga datos estadísticos del sitio web de RNDC."""
    logger.info("Iniciando Playwright para descargar datos de RNDC...")
    browser, context, page = new_rndc_page()

    try:
        page.goto(URL)
        logger.info(f"Navegando a: {URL}")

        # Esperar que cargue el elemento de captcha
        page.wait_for_selector(SELECTOR_CAPTCHA)
        sum_text = page.query_selector(SELECTOR_CAPTCHA).text_content()
        sum_verify = sum_detected(str(sum_text))
        logger.info(f"Captcha resuelto: {sum_verify}")

        # Rellenar el resultado del captcha
        page.fill(SELECTOR_RESULTADO, str(sum_verify))
        logger.info("Resultado del captcha ingresado")

        # Calcular y rellenar la fecha del mes anterior
        year_month = previous_month_year()
        page.fill(SELECTOR_FECHA_INICIAL, year_month)
        logger.info(f"Fecha ingresada: {year_month}")

        # Iniciar descarga
        with page.expect_download() as download_info:
            logger.info("Haciendo clic en el botón de descargar...")
            page.locator(SELECTOR_BT_ESTADISTICAS).click()

        # Guardar archivo descargado
        download = download_info.value
        download.save_as("data/RNDC.xlsx")
        logger.info("✅ Archivo descargado exitosamente en data/RNDC.xlsx")

        page.wait_for_timeout(2000)

    except Exception as e:
        logger.error(f"❌ Error durante la ejecución de Playwright: {e!s}")
        raise

    finally:
        context.close()
        browser.close()
        logger.info("Navegador cerrado")
