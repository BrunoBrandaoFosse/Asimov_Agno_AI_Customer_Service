""""
| ------------------------------------------------------------------------------------------------------------------------------------------- |
| Termo  | O que é                                                                                                                            |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| AMQP   | Um protocolo (padrão de comunicação) para troca de mensagens entre sistemas distribuídos                                           |
| pyamqp | Um driver (implementação em Python) que usa o protocolo AMQP para o Celery se comunicar com o broker (geralmente RabbitMQ)         |
| ------------------------------------------------------------------------------------------------------------------------------------------- |
"""
from celery import Celery
from bot_instance import bot
from logger_config import setup_logger

# Inicializa o logger
logger = setup_logger()

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def task_answer(chat_id, message):
    """Tarefa Celery para enviar uma mensagem via Telegram"""
    # Gera a nova mensagem
    newMsg = f"(você mandou): {message}"

    # Log da mensagem que será enviada
    logger.info(f"Mensagem enviada para {chat_id}: {newMsg}")

    # Enviar a mensagem usando o bot do Telegram
    bot.send_message(chat_id, newMsg)

