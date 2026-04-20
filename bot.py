import os
import telebot
from google import genai
from flask import Flask
import threading

# 1. Serverdagi Environment Variables (Kalitlar)ni o'qish
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 2. Gemini API ulanishi (Yangi kutubxona)
client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot status: Active"

# 3. Telegram bot buyruqlari
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Gemini modelidan javob olish
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xato yuz berdi: {str(e)}")

# 4. Render serveri o'chib qolmasligi uchun parallel funksiya
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    # Flask serverni orqa fonda ishga tushirish
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("Bot ishga tushdi...")
    # Botni ishga tushirish (Polling)
    bot.infinity_polling()
