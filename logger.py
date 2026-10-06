import logging
from pathlib import Path


def setup_logging(output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("bioforge")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(out / "bioforge.log", mode="a", encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(file_handler)

        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(console)

    return logger