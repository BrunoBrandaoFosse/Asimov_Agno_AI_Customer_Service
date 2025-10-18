import os
import telebot
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# Criar instância do bot
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Handler para comando /start
# Quando o usuário inicia o bot, ele recebe uma mensagem de boas-vindas
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    # user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # Aqui você pode salvar em banco de dados ou arquivo
    print(f"Novo usuário: {first_name} - Chat ID: {chat_id}")

    bot.reply_to(message, "Olá! Bem-vindo ao bot.")

# Handler para receber mensagens e responder o usuário
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    texto = message.text
    user_name = message.from_user.first_name
    
    resposta = f"Olá {user_name}! Você disse: {texto}"
    bot.reply_to(message, resposta)

# Função para enviar mensagem diretamente (sem ser resposta)
def enviar_mensagem_direta(chat_id, texto):
    """Envia uma mensagem diretamente para um chat específico"""
    bot.send_message(chat_id, texto)

def run_bot():
    print("Bot está rodando...")
    bot.infinity_polling()
