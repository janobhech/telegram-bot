import telebot
import os
from flask import Flask
from threading import Thread

# 1. Render botni o'chirib qo'ymasligi uchun Flask server
app = Flask('')

@app.route('/')
def home():
    return "Bot status: Online ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Telegram Bot sozlamalari
# Quyidagi qo'shtirnoq ichiga BotFather bergan tokenni yozing!
TOKEN = "8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men Renderda muvaffaqiyatli ishga tushdim! 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Siz yozdingiz: " + message.text)

# 3. Asosiy ishga tushirish qismi
if __name__ == "__main__":
    keep_alive()  # Veb-serverni yoqish
    print("Bot hozir ishga tushdi...")
    bot.infinity_polling() # Botni doimiy aloqada saqlash
