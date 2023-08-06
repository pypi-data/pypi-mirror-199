import logging
import os
from pathlib import Path
from datetime import datetime
from pq_dataset.utils.InputFile import InputFile

def start_logging(output_file: str, debug: bool) -> None:

    logger = logging.getLogger()

    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    # our first handler is a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler_format = '%(asctime)s | %(name)s |  %(levelname)s: %(message)s'
    console_handler.setFormatter(logging.Formatter(console_handler_format))
    logger.addHandler(console_handler)

    # Setting up file handler if debug is true
    if debug:
        output = os.path.expanduser('~')
        log_path = f'{output}{os.path.sep}pqd_logging'

        if not Path(log_path).exists():
            os.makedirs(log_path)

        logfile_name = f'{log_path}{os.path.sep}{datetime.today().strftime("%Y-%m-%d")}_{InputFile(output_file).file_name_wo_ext}.log'
        file_handler = logging.FileHandler(logfile_name)
        file_handler.setLevel(logging.DEBUG)
        file_handler_format = '%(asctime)s | %(levelname)s | %(name)s | %(lineno)d: %(message)s'
        file_handler.setFormatter(logging.Formatter(file_handler_format))
        logger.addHandler(file_handler)

        logger.info(f'Logging started - writing to: {logfile_name}')
    
    return None
