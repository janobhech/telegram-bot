import os
import telebot
import google.generativeai as genai
from flask import Flask

# 1. Serverdagi kalitlarni o'qish (Environment Variables)
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 2. Gemini-ni SOZLASH (Xatoni yo'qotuvchi qism)
genai.configure(api_key=GEMINI_KEY)

# Bu yerda modelni aniq v1 versiyasi bilan chaqiramiz
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash'
)

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot ishlamoqda..."

# 3. Telegram buyruqlari
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Gemini-dan javob olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Agar xato bo'lsa, uni ko'rsatish
        bot.reply_to(message, f"Texnik xato: {str(e)}")

if __name__=="__main__":
    # Botni ishga tushirish
    bot.infinity_polling()
