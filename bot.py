import telebot
import os
from flask import Flask
from threading import Thread

# 1. Flask serverni sozlash (Render o'chirib qo'ymasligi uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Telegram Bot sozlamalari
# DIQQAT: Pastdagi qo'shtirnoq ichiga BotFather bergan tokenni yozing!
TOKEN = "8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA" 
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Bot muvaffaqiyatli ishga tushdi! ✅")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Siz yozdingiz: " + message.text)

# 3. Botni ishga tushirish
if name == "main":
    keep_alive() # Serverni yoqish
    print("Bot ishga tushdi...")
    bot.infinity_polling() # Botni doimiy yoqiq saqlash
