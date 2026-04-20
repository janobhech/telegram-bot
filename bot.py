import os
import telebot
import requests
from flask import Flask
import threading

# 1. Kalitlarni olish (Render Settings/Environment Variables qismidan oladi)
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is active and running!"

# 2. Gemini Pro bilan ulanish funksiyasi
def get_gemini_response(text):
    # Bu model deyarli hamma API kalitlarda standart holatda ochiq bo'ladi
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # Javobni ajratib olish
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in result:
            return f"Google API Xatosi: {result['error']['message']}"
        else:
            return "Kechirasiz, javob olishda noma'lum xatolik yuz berdi."
    except Exception as e:
        return f"Ulanish xatosi: {str(e)}"

# 3. Telegram xabarlarini qayta ishlash
@bot.message_handler(func=lambda message: True)
def chat(message):
    # Foydalanuvchiga "o'ylayotganini" bildirish uchun status yuboramiz
    bot.send_chat_action(message.chat.id, 'typing')
    
    reply = get_gemini_response(message.text)
    bot.reply_to(message, reply)

# 4. Render uchun serverni yoqish
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    # Flaskni alohida oqimda ishga tushiramiz
    threading.Thread(target=run, daemon=True).start()
    print("Bot muvaffaqiyatli ishga tushdi...")
    # Telegramni doimiy polling rejimiga o'tkazamiz
    bot.infinity_polling()
