import pathlib

from datetime import datetime
from loguru import logger


def get_dt() -> str:
    return datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def convert_dt(value: str) -> str:
    dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return dt


log_dir = pathlib.Path.home().joinpath("logs")
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(
    log_dir.joinpath("tcs-database-parser.log"),
    format="{time} [{level}] {module} {name} {function} - {message}",
    level="DEBUG",
    compression="zip",
    rotation="50 MB",
)