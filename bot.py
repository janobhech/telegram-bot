import os
import telebot
import google.generativeai as genai  # Kutubxonaning barqaror versiyasi
from flask import Flask
import threading

# 1. Kalitlarni olish
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 2. Gemini va Botni sozlash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Eng barqaror format
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running live!"

# 3. Chat funksiyasi
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Xabar yuborish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Xato bo'lsa, aniq sababini ko'rsatadi
        bot.reply_to(message, f"Xato: {str(e)}")

# 4. Render serveri uchun
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    threading.Thread(target=run, daemon=True).start()
    print("Bot yoqildi...")
    bot.infinity_polling()
