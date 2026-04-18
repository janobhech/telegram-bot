import os
import telebot
import google.generativeai as genai
from flask import Flask

# 1. SOZLAMALAR (Render'dan olinadi)
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# 2. GEMINI VA BOTNI UALSH
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot ishlamoqda..."

# 3. TELEGRAM BUYRUQLARI
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xato yuz berdi: {e}")

if __name__=="__main__":
    bot.infinity_polling()
