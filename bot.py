import os
import telebot
from google import genai
from flask import Flask
import threading

# 1. Kalitlarni serverdan olish
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 2. Yangi Gemini SDK ulanishi
client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot ishlamoqda..."

# 3. Bot mantiqi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Yangi kutubxona bo'yicha so'rov yuborish
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xato: {str(e)}")

# Render uchun parallel server funksiyasi
def run_flask():
    # Render avtomatik beradigan portni olamiz
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    # Flaskni orqa fonda (threading) ishga tushirish
    threading.Thread(target=run_flask).start()
    print("Bot ishga tushdi...")
    # Botni asosiy yo'nalishda ishga tushirish
    bot.infinity_polling()
