from logger_config import setup_logger
from bot_instance import bot
from workers import tasks

# Inicializa o logger
logger = setup_logger()

# --------------------------------------------------------------------------

# Handler para comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Envia uma mensagem de boas-vindas ao usuário que inicia o bot"""
    chat_id = message.chat.id
    # user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # Aqui você pode salvar em banco de dados ou arquivo
    logger.info(f"Novo usuário: {first_name} - Chat ID: {chat_id}")

    bot.reply_to(message, "Olá! Bem-vindo ao bot.")

# --------------------------------------------------------------------------

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Manipula mensagens recebidas e responde ao usuário"""
    msg = message.text
    user_name = message.from_user.first_name

    # Gera a resposta
    # resposta = f"Olá {user_name}! Você disse: {msg}"
    # bot.reply_to(message, resposta)

    logger.info(f"Recebida mensagem de {user_name}: {msg}")

    # Envia a tarefa para o Celery processar a resposta
    tasks.task_answer.delay(message.chat.id, msg)

# --------------------------------------------------------------------------

def send_direct_message(chat_id, texto):
    """Envia uma mensagem diretamente para um chat específico"""
    bot.send_message(chat_id, texto)

def run_bot():
    """Inicia o bot do Telegram"""
    logger.info("Bot está rodando...")
    bot.infinity_polling()
