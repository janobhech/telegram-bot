import os
import telebot
import requests
from flask import Flask
import threading
import time

# 1. Kalitlar (Render-dagi Environment Variables-dan oladi)
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot status: Online"

def get_gemini_response(text):
    # Sizning rasmda ko'ringan model nomi
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": text}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            # Agar Google 2.5-ni hali API-da "topilmadi" desa, 1.5-ni sinab ko'radi
            return f"Google xatosi: {result['error']['message']}"
        return "Javob olishda xatolik yuz berdi."
    except Exception as e:
        return f"Ulanish xatosi: {str(e)}"

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = get_gemini_response(message.text)
    bot.reply_to(message, reply)

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            time.sleep(5)
