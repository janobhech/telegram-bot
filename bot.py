import telebot
import os
from flask import Flask
from threading import Thread

# 1. FLASK SERVER QISMI (Botni uyg'oq saqlash uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render PORTni avtomatik beradi, agar bo'lmasa 10000 ishlatiladi
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. TELEGRAM BOT QISMI
TOKEN = 'SIZNING_BOT_TOKENINGIZ' # <--- Tokeningizni shu yerga qo'ying
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men yuridik botman va endi doim uyg'oqman!")

# 3. ISHGA TUSHIRISH
if __name__=="__main__":
    print("Bot ishga tushmoqda...")
    keep_alive()  # <--- Flask serverni alohida oqimda yurgizadi
    bot.infinity_polling() # <--- Botni tinimsiz ishlatadi
