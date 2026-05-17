from app.config.settings import settings
from app.core.logging import get_app_logger
from app.core.monitoring import init_monitoring

logger = get_app_logger("")


def main():
    init_monitoring(dsn=settings.sentry_dsn, environment=settings.environment)
    logger.info("Hello World")


if __name__ == "__main__":
    main()
