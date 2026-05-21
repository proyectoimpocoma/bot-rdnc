
"""Módulo principal para ejecutar el bot de scrapping de RDNC y SICETAC."""

from datetime import date
import os

from app.core.logging import get_app_logger
from app.scrapper import playwright_rndc
from app.UI.chat_page import render
import asyncio

logger = get_app_logger("main")


def main():
    render()

    if date.today().day == 1 or os.path.exists("data/RNDC.xlsx") is False:
        try:
            asyncio.run(playwright_rndc())
        except Exception as e:
            logger.error(f"Error ejecutando playwright_rndc: {e!s}")


if __name__ == "__main__":
    main()
