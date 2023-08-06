import logging
from importlib.metadata import version
from pathlib import Path

NAME = "kayak"
__version__ = VERSION = version(NAME)


def get_home() -> Path:
    user_home = Path.home()
    app_home = user_home.joinpath("." + NAME)
    if not app_home.exists():
        app_home.mkdir()
    return app_home


LOG = get_home().joinpath(NAME + ".log")

logger_handler = logging.FileHandler(LOG)
logger_handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s"))

logger = logging.getLogger()
logger.addHandler(logger_handler)
logger.setLevel(logging.INFO)
