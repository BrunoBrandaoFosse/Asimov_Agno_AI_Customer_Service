from contextlib import asynccontextmanager
from logger_config import setup_logger
import threading
from fastapi import FastAPI
from routers import telegram_router_v2
from services import telegram_bot

# Inicializa o logger
logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_thread = threading.Thread(target=telegram_bot.run_bot, name="TelegramBotThread")
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
    return {"api": "Agente de IA para Atendimento no Telegram"}
