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

    # Configura o logger raiz
    logging.basicConfig(
        level=level,
        handlers=[handler]
    )

    # Retorna o logger padrão (raiz)
    return logging.getLogger()
