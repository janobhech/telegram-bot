import telebot
import os
from flask import Flask
from threading import Thread

# 1. Render uchun Flask server
app = Flask('')

@app.route('/')
def home():
    return "Yuridik Bot Online ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot sozlamalari
# DIQQAT: BotFather bergan tokenni mana shu qo'shtirnoq ichiga yozing!
TOKEN = "8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA" 
bot = telebot.TeleBot(TOKEN)

# Asosiy Menyu Tugmalari
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("⚖️ Huquqiy savol-javob")
    item2 = telebot.types.KeyboardButton("📝 Da'vo ariza namunalari")
    item3 = telebot.types.KeyboardButton("📜 Shartnomalar")
    markup.add(item1, item2, item3)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men yuridik yordamchi botman. Kerakli bo'limni tanlang:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def yuridik_bot(message):
    msg = message.text

    # 1. Da'vo arizalari bo'limi
    if msg == "📝 Da'vo ariza namunalari":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("💔 Aliment undirish", "🏠 Uyga kiritish", "💼 Ishga tiklanish", "⬅️ Orqaga")
        bot.send_message(message.chat.id, "Qaysi turdagi ariza namunasi kerak?", reply_markup=markup)

    elif msg == "💔 Aliment undirish":
        text = (
            "🏛 Aliment undirish haqida da'vo ariza (Namuna):\n\n"
            "Fuqarolik ishlari bo'yicha _____ tuman sudiga\n"
            "Da'vogar: _____ (F.I.SH., manzili)\n"
            "Javobgar: _____ (F.I.SH., manzili)\n\n"
            "DA'VO ARIZA\n"
            "Oila kodeksining 96-moddasiga asosan, javobgardan bir nafar farzandimiz ta'minoti uchun daromadining 1/4 qismi miqdorida aliment undirishingizni so'rayman."
        )
        bot.send_message(message.chat.id, text)

    # 2. Huquqiy savollar
    elif msg == "⚖️ Huquqiy savol-javob":
        bot.send_message(message.chat.id, "Savolingizni yozing (masalan: Jarima, Ish haqi, Ta'til).")

    elif "jarima" in msg.lower():
        bot.reply_to(message, "🚫 15 kun ichida to'langan jarimalar uchun 50% chegirma mavjud.")

    elif "ish haqi" in msg.lower():
        bot.reply_to(message, "💼 Mehnat kodeksiga ko'ra, ish haqi har yarim oyda bir marta to'lanishi shart.")

    # Orqaga qaytish
    elif msg == "⬅️ Orqaga":
        bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=main_menu())

    else:
        bot.reply_to(message, "Tushunmadim. Iltimos, menyudagi tugmalardan foydalaning.")
if __name__ == "__main__":
    keep_alive()  # Veb-serverni yoqish
    print("Bot hozir ishga tushdi...")
    bot.infinity_polling() # Botni doimiy aloqada saqlash
