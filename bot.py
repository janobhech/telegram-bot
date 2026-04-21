import os
import telebot
import requests
from flask import Flask
import threading
import time

# Kalitlar (Render Environment Variables-dan olinadi)
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot status: Online"

def get_gemini_response(text):
    # Har ehtimolga qarshi bir nechta model nomini sinab ko'ramiz
    # Agar 2.5 ishlamasa, avtomatik 1.5 ga o'tadi
    models = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-pro"]
    
    uzbek_instruction = "Sening isming Gemini. Iltimos, barcha savollarga faqat o'zbek tilida javob ber. "
    full_prompt = uzbek_instruction + text

    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if "candidates" in result:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            # Agar bu modelda xato bo'lsa, keyingisiga o'tadi
            continue
        except:
            continue
            
    return "❌ Kechirasiz, hozirda Google tizimiga ulanishda muammo bor. API kalitingizni va Render sozlamalarini tekshiring."

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
