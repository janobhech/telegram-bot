pyTelegramBotAPI
flask
import telebot
import os
from flask import Flask
from threading import Thread

# 1. Renderni aldash uchun kichik server
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render beradigan PORTni yoki 8080 ni ishlatamiz
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Botingizning asosiy qismi
TOKEN = "pyTelegramBotAPI
flask
import telebot
import os
from flask import Flask
from threading import Thread

# 1. Renderni aldash uchun kichik server
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render beradigan PORTni yoki 8080 ni ishlatamiz
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Botingizning asosiy qismi
TOKEN = ""
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Renderda tekin va xatosiz ishlayapman! ✅")

# Bu yerga boshqa kodlaringizni (yurist bot funksiyalarini) qo'shishingiz mumkin

# 3. Botni va Serverni birga yurgizish
if name == "main":
    keep_alive()  # Serverni fonda yoqadi (Render xursand bo'ladi)
    print("Bot ishga tushdi...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Renderda tekin va xatosiz ishlayapman! ✅")

# Bu yerga boshqa kodlaringizni (yurist bot funksiyalarini) qo'shishingiz mumkin

# 3. Botni va Serverni birga yurgizish
if name == "main":
    keep_alive()  # Serverni fonda yoqadi (Render xursand bo'ladi)
    print("Bot ishga tushdi...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
