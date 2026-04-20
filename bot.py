import os
import telebot
from google import genai
from flask import Flask
import threading

# 1. Kalitlarni tizimdan olish
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 2. Yangi Gemini va Telegram ulanishi
client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is live and running!"

# 3. Savol-javob mantiqi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI botman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Yangi kutubxona mantiqi
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xato yuz berdi: {str(e)}")

# 4. Render uchun Port va Threading
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    # Flaskni parallel yoqish
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot ishga tushdi...")
    # Telegramni yoqish
    bot.infinity_polling()
