import logging
from pathlib import Path
def create_output_dir(output_dir ) :
    output_dir = Path(output_dir )
    output_dir.mkdir(parents=True, exist_ok= True)
    return output_dir

def setup_logging(output_dir) :
    output_dir = create_output_dir(output_dir)
    log_path = output_dir / "bioforge.log"
    log_config=  {
        "filename":log_path,
        "filemode": "a",
        "level": logging.INFO,
        "format": "{asctime} - {levelname} - {message}",
        "style": "{"
    }
    logging.basicConfig(**log_config)

    return logging.getLogger ("BioForge")