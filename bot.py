import os
import telebot
import requests
from flask import Flask
import threading

# 1. Kalitlarni olish
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is active"

# 2. To'g'ridan-to'g'ri API orqali Gemini bilan gaplashish
def get_gemini_response(text):
    # Bu yerda v1beta emas, balki v1 (barqaror) versiyadan foydalanamiz
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # Javobni olish mantiqi
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Xato: {result}"

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        reply = get_gemini_response(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ulanishda xato: {str(e)}")

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__=="__main__":
    threading.Thread(target=run, daemon=True).start()
    bot.infinity_polling()
