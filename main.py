from app.bot.handler import BotHandler
from app.core.logging import get_app_logger

logger = get_app_logger("")


def main():
    bot = BotHandler()
    resultado = bot.run("De Abejorral a Guarne")
    logger.info(resultado)


if __name__ == "__main__":
    main()
