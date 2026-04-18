import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import os

# 1. MAXFIY MA'LUMOTLARNI TIZIMDAN OLISH
# Bu nomlar Render'dagi "Key" ustunidagi nomlar bilan bir xil bo'lishi shart
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# AI va Botni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 2. RENDER UCHUN SERVER (O'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home():
    return "Bot Online ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. BOT FUNKSIYALARI
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Savolingizni yozing, men yuridik AI yordamchingizman.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        prompt = f"O'zbekiston qonunchiligi asosida javob ber: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Hozircha javob bera olmayman. Render'dagi Environment Variables'ni tekshiring.")

if __name__ =="__main__":
    keep_alive()
    bot.infinity_polling()
