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
    return "Bot status: Online"

def get_gemini_response(text):
    # Eng yangi flash modelini sinab ko'ramiz
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": text}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # 1. Muvaffaqiyatli javob kelsa
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        
        # 2. Google xato qaytarsa (Diagnostika qismi)
        elif "error" in result:
            err_msg = result['error']['message']
            if "location is not supported" in err_msg.lower():
                return "❌ MINTAQAVIY CHEKLOV: Render serveri joylashgan hududda Google Gemini ishlamaydi. Server hududini (Region) o'zgartirib ko'ring."
            if "API key not valid" in err_msg:
                return "❌ API KEY XATOSI: Google AI Studio'dan olingan kalit noto'g'ri yoki Render'ga noto'g'ri kiritilgan."
            return f"❌ GOOGLE XATOSI: {err_msg}"
            
        return f"❌ NOMA'LUM XATO: {str(result)}"
        
    except Exception as e:
        return f"❌ ULANISH XATOSI: {str(e)}"

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = get_gemini_response(message.text)
    bot.reply_to(message, reply)

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    threading.Thread(target=run_flask).start()
    print("Veb-server tayyor...")
    
    # Conflict xatosini yengish uchun takroriy urinish
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except:
            time.sleep(5)
