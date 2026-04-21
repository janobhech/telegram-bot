import os
import telebot
import requests
from flask import Flask
import threading
import time

# Kalitlar
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot status: Online"

def get_gemini_response(text):
    # Sizda bor bo'lishi mumkin bo'lgan barcha modellar ro'yxati
    models = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-pro"]
    
    uzbek_instruction = "Sening isming Gemini. Iltimos, barcha savollarga faqat o'zbek tilida javob ber. "
    full_prompt = uzbek_instruction + text

    for model_name in models:
        # MUHIM: v1beta ishlatamiz, chunki 1.5 va 2.5 modellar faqat shu yerda
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=15)
            result = response.json()
            
            if "candidates" in result:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Agar limit tugasa
            if "error" in result and "429" in str(result.get("error", {}).get("code", "")):
                return "⚠️ Limit tugadi (minutiga 5 ta so'rov). 1 daqiqa kuting."
                
        except Exception:
            continue
            
    return "❌ Hozircha Google javob bermayapti. Birozdan so'ng qayta urinib ko'ring."

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        reply = get_gemini_response(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        print(f"Xato: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception:
            time.sleep(5)
