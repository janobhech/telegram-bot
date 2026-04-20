import os
import telebot
import requests
from flask import Flask
import threading

# Kalitlar
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is live!"

def get_gemini_response(text):
    # DIQQAT: Bu URL v1 emas, v1beta va gemini-1.5-flash ishlatadi
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            # Xatolikni aniq ko'rish uchun
            return f"Google API Xatosi: {result['error']['message']}"
        else:
            return "Xato: Google'dan noto'g'ri javob keldi."
    except Exception as e:
        return f"Ulanish xatosi: {str(e)}"

@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = get_gemini_response(message.text)
    bot.reply_to(message, reply)

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

if __name__=="__main__":
    threading.Thread(target=run, daemon=True).start()
    print("Bot ishga tushdi...")
    bot.infinity_polling()
