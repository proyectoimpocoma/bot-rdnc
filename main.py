from app.core.logging import get_app_logger
from app.UI import render
from app.scrapper import playwright_rndc
from datetime import date

from app.scrapper.browser import new_rndc_page
from app.scrapper.utils import sum_detected
from app.scrapper.selectors import (
    URL_SICETAC,
    SELECTOR_CONFIG_VEHICULO,
    SELECTOR_CONDICION_CARGA,
    SELECTOR_TIPO_CARGA,
    SELECTOR_ORIGEN_VIAJE,
    SELECTOR_DESTINO_VIAJE,
    SELECTOR_HORAS_CARGUE,
    SELECTOR_HORAS_DESCARGUE,
    SELECTOR_CARROCERIA_VEHICULO,
    SELECTOR_CAPTCHA,
    SELECTOR_RESULTADO_CAPTCHA,
    SELECTOR_BT_CALCULAR,
    SELECTOR_COSTO_TOTAL_VIAJE,
)

logger = get_app_logger("main")


def playwright_sicetac():
    """Función placeholder para el scrapper de SICETAC."""
    logger.info("playwright_sicetac aún no implementado.")
    browser, context, page = new_rndc_page()
    try:
        page.goto(URL_SICETAC)
        logger.info(f"Navegando a: {URL_SICETAC}")

        config_vehiculo = page.locator(SELECTOR_CONFIG_VEHICULO).select_option(
            "Tractocamión tres ejes con semiremolque de tres ejes"
        )

        condicion_carga = page.locator(SELECTOR_CONDICION_CARGA).select_option(
            "CARGADO"
        )

        carroceria_vehiculo = page.locator(SELECTOR_CARROCERIA_VEHICULO).select_option(
            "ESTACAS"
        )
        tipo_carga = page.locator(SELECTOR_TIPO_CARGA).select_option("General")

        origen_viaje = page.locator(SELECTOR_ORIGEN_VIAJE).select_option(
            "ABEJORRAL - ABEJORRAL - ANTIOQUIA"
        )

        destino_viaje = page.locator(SELECTOR_DESTINO_VIAJE).select_option(
            "GUARNE - GUARNE - ANTIOQUIA"
        )

        horas_cargue = page.locator(SELECTOR_HORAS_CARGUE).fill("4")
        horas_descargue = page.locator(SELECTOR_HORAS_DESCARGUE).fill("4")

        capcha_text = page.locator(SELECTOR_CAPTCHA).text_content()
        sum_captcha = sum_detected(str(capcha_text))

        page.locator(SELECTOR_RESULTADO_CAPTCHA).fill(str(sum_captcha))

        page.locator(SELECTOR_BT_CALCULAR).click()

        result = page.wait_for_selector(SELECTOR_COSTO_TOTAL_VIAJE).input_value()
        logger.info(f"Resultado del cálculo: {result}")

    except Exception as e:
        logger.error(f"Error en playwright_sicetac: {e!s}")
        return False
    finally:
        context.close()
        browser.close()
        logger.info("Navegador cerrado en playwright_sicetac.")


def main():
    render()

    if date.today().day == 1:
        try:
            playwright_rndc()
        except Exception as e:
            logger.error(f"Error ejecutando playwright_rndc: {e!s}")

    try:
        playwright_sicetac()
    except Exception as e:
        logger.error(f"Error ejecutando playwright_sicetac: {e!s}")


if __name__ == "__main__":
    main()
