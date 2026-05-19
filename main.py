from app.core.logging import get_app_logger
from app.UI import render
from app.scrapper import playwright_rndc
from datetime import date


logger = get_app_logger("main")


URL = "https://plc.mintransporte.gov.co/Runtime/empresa/ctl/SiceTAC/mid/417"


def playwright_sicetac():
    """Función placeholder para el scrapper de SICETAC."""
    logger.info("playwright_sicetac aún no implementado.")


def main():
    render()
    if date.today().day == 1:
        playwright_rndc()

    playwright_sicetac()


if __name__ == "__main__":
    main()
