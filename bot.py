import telebot
import os
from flask import Flask
from threading import Thread

# 1. Flask server (Render uchun)
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
# O'zingizning TOKENingizni qo'yishni unutmang!
TOKEN = "712345678:ABCDefgh..." 
bot = telebot.TeleBot(TOKEN)

# Start komandasi uchun menyu
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("💼 Mehnat huquqi")
    item2 = telebot.types.KeyboardButton("🏠 Oila huquqi")
    item3 = telebot.types.KeyboardButton("📄 Shartnomalar")
    item4 = telebot.types.KeyboardButton("🚫 Jarimalar")
    markup.add(item1, item2, item3, item4)
    
    bot.reply_to(message, "Assalomu alaykum! Men yuridik maslahatchi botman. Quyidagi mavzulardan birini tanlang yoki savolingizni yozing:", reply_markup=markup)

# Aqlli javob berish tizimi
@bot.message_handler(func=lambda message: True)
def yuridik_maslahat(message):
    savol = message.text.lower()

    # Mehnat huquqi
    if "mehnat" in savol or "ishdan bo'shash" in savol or "ish haqi" in savol:
        bot.reply_to(message, "⚖️ Mehnat masalalari:\n1. Ishdan bo'shash uchun 2 hafta oldin ariza beriladi.\n2. Ish haqi kechiktirilganda Davlat mehnat inspeksiyasiga murojaat qiling.\n3. Ta'til muddati kamida 15 ish kunidan iborat bo'lishi kerak.")

    # Oila huquqi
    elif "oila" in savol or "ajrim" in savol or "aliment" in savol:
        bot.reply_to(message, "👨‍👩‍👧‍👦 Oila masalalari:\n1. Aliment miqdori: 1 bola uchun 25%, 2 bola uchun 33%, 3 va undan ko'p uchun 50%.\n2. Ajrim sud orqali yoki FXDY (ZAGS) orqali amalga oshiriladi.\n3. Nikoh shartnomasi ixtiyoriy hisoblanadi.")

    # Shartnomalar
    elif "shartnoma" in savol or "ijara" in savol:
        bot.reply_to(message, "📜 Shartnoma va Ijara:\n1. Ijara shartnomasi soliq idoralarida ro'yxatdan o'tishi shart (ijara.soliq.uz).\n2. Qarz shartnomasi 10 baravar BHMdan ko'p bo'lsa, yozma tuzilishi shart.")

    # Jarimalar
    elif "jarima" in savol or "qoidabuzar" in savol:
        bot.reply_to(message, "🚫 Jarimalar:\n1. Jarimani 15 kun ichida to'lasangiz, 50% chegirma mavjud.\n2. Jarimalarni @e_jarima_bot yoki my.gov.uz orqali tekshirish mumkin.")

    # Salomlashish
    elif "salom" in savol or "assalom" in savol:
        bot.reply_to(message, "Vaalaykum assalom! Savolingizni mavzular bo'yicha bersangiz, aniqroq javob beraman.")

    # Tushunilmagan holat
    else:
        bot.reply_to(message, "😔 Kechirasiz, men hozircha bu savolga javob bera olmayman. Iltimos, 'Mehnat', 'Oila', 'Aliment' yoki 'Jarima' so'zlari ishtirokida savol bering.")

# 3. Asosiy ishga tushirish qismi
if __name__ == "__main__":
    keep_alive()  # Veb-serverni yoqish
    print("Bot hozir ishga tushdi...")
    bot.infinity_polling() # Botni doimiy aloqada saqlash
