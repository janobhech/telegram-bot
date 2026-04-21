import os
import telebot
import requests
from flask import Flask
import threading
import time

# 1. Kalitlar (Render Environment Variables'dan olinadi)
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot status: Online"

def get_gemini_response(text):
    # Eng yangi va barqaror model versiyasi
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": text}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # Muvaffaqiyatli javob kelsa
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        
        # Agar Google xato qaytarsa, aniq sababini ko'rsatadi
        elif "error" in result:
            return f"❌ Google API Xatosi: {result['error']['message']}"
            
        return f"❌ Noma'lum xato yuz berdi: {str(result)}"
        
    except Exception as e:
        return f"❌ Ulanishda xato: {str(e)}"

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = get_gemini_response(message.text)
    bot.reply_to(message, reply)

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    # Render uchun veb-serverni ishga tushirish
    threading.Thread(target=run_flask, daemon=True).start()
    print("Veb-server ishga tushdi...")
    
    # Conflict (409) xatosini chetlab o'tish uchun
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Polling xatosi: {e}")
            time.sleep(5)
