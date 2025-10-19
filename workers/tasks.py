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
from redisvl.extensions.cache.llm import SemanticCache

# Inicializa o logger
logger = setup_logger()

app = Celery('tasks', broker='pyamqp://guest@localhost//')

_cache = None # Singleton do cache semântico RedisVL
_agent = None # Singleton do agente AI

# --------------------------------------------------------------------------

# Singleton do cache semântico RedisVL
def get_cache():
    global _cache
    if _cache is None:
        _cache = connect_semantic_cache()
    return _cache

# --------------------------------------------------------------------------

# Singleton do agente AI
def get_agent():
    global _agent

    if _agent is None:
        # Carrega documento asimov.md
        with open("data/asimov.md", "r") as f:
            asimov_doc = f.read()

        # Carrega documento prompt.xml
        with open("data/prompt.xml", "r") as f:
            prompt_doc = f.read()
        
        # Inicializa o agente
        _agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini"),
            instructions=f"<fatos>{asimov_doc}</fatos>{prompt_doc}",
        )

    return _agent

# --------------------------------------------------------------------------

@app.task
def task_answer(chat_id: int, prompt: str):
    """Tarefa Celery para enviar uma mensagem via Telegram"""

    cache = get_cache()
    
    # Verifica se há resposta no cache semântico
    # := Operador Walrus do Python 3.8+. Atribui e avalia ao mesmo tempo
    if response := get_semantic_cache_answer(cache, prompt):
        logger.info(f"Resposta obtida do cache semântico para chat_id {chat_id}")
        message = f"(cache) {response}"
    else:
        # Obter a resposta do agente AI
        message = get_ai_answer(prompt=prompt)
        if message:
            # Armazena a resposta no cache semântico
            set_semantic_cache_answer(cache=cache, prompt=prompt, answer=message)
        else:
            # Mensagem padrão caso ocorra algum erro em get_ai_answer
            message = "Tente novamente mais tarde."

    # Log da mensagem que será enviada
    logger.info(f"Mensagem enviada para {chat_id}: {message}")

    # Enviar a mensagem usando o bot do Telegram
    bot.send_message(chat_id, message)

# --------------------------------------------------------------------------

def get_semantic_cache_answer(cache: SemanticCache, prompt: str) -> str | None:
    """Obtém resposta do cache semântico RedisVL"""

    # Verifica se o cache está inicializado
    if cache is None:
        print("⚠️ Cache não inicializado!")
        return None
    
    # Verifica se há resposta no cache
    response = cache.check(prompt=prompt)

    # Retorna a primeira resposta se existir
    if len(response) == 0:
        return None
    
    return response[0]['response']

# --------------------------------------------------------------------------

def set_semantic_cache_answer(cache: SemanticCache, prompt: str, answer: str) -> None:
    """Armazena a resposta no cache semântico RedisVL"""
    cache.store(prompt=prompt, response=answer)

# --------------------------------------------------------------------------

def get_ai_answer(prompt: str) -> str:
    try:
        agent = get_agent()
        result = agent.run(prompt)
        return result.content
    except Exception as e:
        logger.error(f"Erro ao obter resposta do agente: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação."

# --------------------------------------------------------------------------

def connect_semantic_cache():
    """Conecta ao cache semântico RedisVL"""
    return SemanticCache(
        name="llmcache",                        # nome do índice de pesquisa subjacente
        ttl=86400,                              # tempo de vida em segundos
        redis_url="redis://localhost:6379",     # url de conexão Redis
        distance_threshold=0.2,                 # limiar de distância do cache semântico
    )
