from contextlib import asynccontextmanager
import threading
import logging
import colorlog
from fastapi import FastAPI
from routers import telegram_router_v2
from routers import telegram_router

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

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_thread = threading.Thread(target=telegram_router.run_bot, name="TelegramBotThread")
    bot_thread.start()
    yield  # Aqui a aplicação inicia
    # Aqui você pode adicionar código para shutdown se necessário

app = FastAPI(
    title="Agente de IA para Atendimento no Telegram",
    description="Agente de IA para atendimento ao cliente com Agno, Docker, RedisVL (para cache semântico)",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(telegram_router_v2.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
