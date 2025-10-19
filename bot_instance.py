import os
import telebot
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(TELEGRAM_API_KEY)
