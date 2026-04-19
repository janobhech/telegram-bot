import os
import telebot
import google.generativeai as genai
from flask import Flask

# 1. SOZLAMALAR (Serverdan olinadi)
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# 2. GEMINI VA BOTNI SOZLASH
genai.configure(api_key=GEMINI_API_KEY)
# Bu qator 404 xatosini yo'qotadi:
model = genai.GenerativeModel('models/gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running..."

# 3. BOT BUYRUQLARI
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Gemini javobini olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Xatoni aniq ko'rsatish
        bot.reply_to(message, f"Texnik xato yuz berdi: {str(e)}")

if __name__=="__main__":
    # Server portini aniqlash
    port = int(os.environ.get("PORT", 8080))
    # Botni ishga tushirish (Polling)
    bot.infinity_polling()
