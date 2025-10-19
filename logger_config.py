import logging
import colorlog

def setup_logger(level=logging.INFO):
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    ))

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers = []  # Remove outros handlers
    logger.addHandler(handler)
    return logger
