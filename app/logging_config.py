import logging
from pathlib import Path


LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "minigpt.log"


def configure_logging():
    LOG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )

    logging.getLogger("httpx").setLevel(
        logging.WARNING
    )


logger = logging.getLogger("minigpt")
