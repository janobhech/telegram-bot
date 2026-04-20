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
    return "Bot is live and running!"

# 2. Siz so'ragan Gemini Pro funksiyasi
def get_gemini_response(text):
    # Eng barqaror model va versiya kombinatsiyasi
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"
    
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
            return f"Google API Xatosi: {result['error']['message']}"
        else:
            return "Xato: Noma'lum muammo yuz berdi."
    except Exception as e:
        return f"Ulanish xatosi: {str(e)}"

# 3. Telegram xabarlarini qabul qilish
@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply = get_gemini_response(message.text)
    bot.reply_to(message, reply)

# 4. Render serveri uchun qism
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    threading.Thread(target=run, daemon=True).start()
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
