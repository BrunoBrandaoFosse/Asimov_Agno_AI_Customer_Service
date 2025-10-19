""""
| ------------------------------------------------------------------------------------------------------------------------------------------- |
| Termo  | O que é                                                                                                                            |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| AMQP   | Um protocolo (padrão de comunicação) para troca de mensagens entre sistemas distribuídos                                           |
| pyamqp | Um driver (implementação em Python) que usa o protocolo AMQP para o Celery se comunicar com o broker (geralmente RabbitMQ)         |
| ------------------------------------------------------------------------------------------------------------------------------------------- |
"""
from celery import Celery, signals
from bot_instance import bot
from logger_config import setup_logger
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Inicializa o logger
logger = setup_logger()

app = Celery('tasks', broker='pyamqp://guest@localhost//')

agent = None

@signals.worker_process_init.connect
def on_worker_process_init(**kwargs):
    """
    Sinal para inicialização do processo do trabalhador
    Esta função é chamada quando o processo do trabalhador Celery é iniciado.
    """
    logger.info("Processo do trabalhador iniciado")

    # Inicializa o agente globalmente quando o trabalhador inicia
    global agent

    # Carrega documento asimov.md
    with open("data/asimov.md", "r") as f:
        asimov_doc = f.read()

    # Carrega documento prompt.xml
    with open("data/prompt.xml", "r") as f:
        prompt_doc = f.read()

    # Inicializa o agente
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        instructions=f"<fatos>{asimov_doc}</fatos>{prompt_doc}",
    )

@app.task
def task_answer(chat_id, message):
    """Tarefa Celery para enviar uma mensagem via Telegram"""

    # Obter a resposta do agente AI
    result = get_ai_answer(prompt=message)

    # Log da mensagem que será enviada
    logger.info(f"Mensagem enviada para {chat_id}: {result}")

    # Enviar a mensagem usando o bot do Telegram
    bot.send_message(chat_id, result)

def get_ai_answer(prompt):
    try:
        result = agent.run(prompt)
        return result.content
    except Exception as e:
        logger.error(f"Erro ao obter resposta do agente: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação."
