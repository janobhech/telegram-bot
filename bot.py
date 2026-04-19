import os
import telebot
import google.generativeai as genai
from flask import Flask

# 1. Serverdagi kalitlarni o'qish
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 2. Gemini-ni sozlash (404 xatosini oldini olish uchun models/ qo'shilgan)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot ishlamoqda..."

# 3. Bot buyruqlari
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xato yuz berdi: {str(e)}")

if __name__=="__main__":
    # Botni ishga tushirish
    bot.infinity_polling()
