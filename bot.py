import os
import telebot
import requests
from flask import Flask
import threading
import time

# 1. Kalitlar
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is active!"

def get_gemini_response(text):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": text}]}]}
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        return "Xato: Gemini javob bermadi."
    except:
        return "Ulanishda xato."

@bot.message_handler(func=lambda message: True)
def chat(message):
    reply = get_gemini_response(message.text)
    bot.reply_to(message, reply)

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    # Avval Flaskni ishga tushiramiz (Render uchun)
    threading.Thread(target=run_flask).start()
    
    print("Veb-server ishga tushdi, bot ulanmoqda...")
    time.sleep(2) # Kichik tanaffus

    # Conflict xatosini yengish uchun pollingni qayta-qayta urinib ko'ramiz
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60)
        except Exception as e:
            print(f"Pollingda xato: {e}. 5 soniyadan keyin qayta urinish...")
            time.sleep(5)
