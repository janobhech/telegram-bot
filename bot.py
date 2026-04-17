[17.04.2026 19:39] Ilyoz bek: import telebot
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
TOKEN = "8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA" 
bot = telebot.TeleBot(TOKEN)

# Asosiy Menyu (Tugmalar)
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("⚖️ Huquqiy savol-javob")
    item2 = telebot.types.KeyboardButton("📝 Da'vo ariza namunalari")
    item3 = telebot.types.KeyboardButton("📜 Shartnomalar")
    markup.add(item1, item2, item3)
    
    bot.reply_to(message, "Assalomu alaykum! Men sizning shaxsiy yuridik yordamchingizman. Kerakli bo'limni tanlang:", reply_markup=markup)

# Xabarlarni qayta ishlash
@bot.message_handler(func=lambda message: True)
def yuridik_bot(message):
    msg = message.text

    # 1-Bo'lim: Da'vo arizalari
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
            "Biz javobgar bilan __-yilda nikohdan o'tganmiz. O'rtamizda __ (farzand ismi) bor. "
            "Hozirda javobgar moddiy yordam bermayapti. Oila kodeksining 96-moddasiga asosan...\n\n"
            "Sizdan so'rayman:\n"
            "Javobgardan bir nafar farzandimiz ta'minoti uchun daromadining 1/4 qismi miqdorida aliment undirishingizni."
        )
        bot.send_message(message.chat.id, text)

    # 2-Bo'lim: Huquqiy savollar (Avvalgi darsdagi kabi)
    elif msg == "⚖️ Huquqiy savol-javob":
        bot.send_message(message.chat.id, "Savolingizni yozing (masalan: Jarima, Ish haqi, Ta'til).")

    elif "jarima" in msg.lower():
        bot.reply_to(message, "🚫 15 kun ichida to'langan jarimalar uchun 50% chegirma bor.")

    elif msg == "⬅️ Orqaga":
        welcome(message)

    else:
        bot.reply_to(message, "Tushunmadim. Iltimos, menyudagi tugmalardan foydalaning yoki aniqroq savol bering.")

# 3. Ishga tushirish
if name == "main":
    keep_alive()
    bot.infinity_polling()
[17.04.2026 19:39] Ilyoz bek: import telebot
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
TOKEN = "SIZNING_TOKENINGIZ" 
bot = telebot.TeleBot(TOKEN)

# Asosiy Menyu (Tugmalar)
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("⚖️ Huquqiy savol-javob")
    item2 = telebot.types.KeyboardButton("📝 Da'vo ariza namunalari")
    item3 = telebot.types.KeyboardButton("📜 Shartnomalar")
    markup.add(item1, item2, item3)
    
    bot.reply_to(message, "Assalomu alaykum! Men sizning shaxsiy yuridik yordamchingizman. Kerakli bo'limni tanlang:", reply_markup=markup)

# Xabarlarni qayta ishlash
@bot.message_handler(func=lambda message: True)
def yuridik_bot(message):
    msg = message.text

    # 1-Bo'lim: Da'vo arizalari
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
            "Biz javobgar bilan __-yilda nikohdan o'tganmiz. O'rtamizda __ (farzand ismi) bor. "
            "Hozirda javobgar moddiy yordam bermayapti. Oila kodeksining 96-moddasiga asosan...\n\n"
            "Sizdan so'rayman:\n"
            "Javobgardan bir nafar farzandimiz ta'minoti uchun daromadining 1/4 qismi miqdorida aliment undirishingizni."
        )
        bot.send_message(message.chat.id, text)

    # 2-Bo'lim: Huquqiy savollar (Avvalgi darsdagi kabi)
    elif msg == "⚖️ Huquqiy savol-javob":
        bot.send_message(message.chat.id, "Savolingizni yozing (masalan: Jarima, Ish haqi, Ta'til).")

    elif "jarima" in msg.lower():
        bot.reply_to(message, "🚫 15 kun ichida to'langan jarimalar uchun 50% chegirma bor.")

    elif msg == "⬅️ Orqaga":
        welcome(message)

    else:
        bot.reply_to(message, "Tushunmadim. Iltimos, menyudagi tugmalardan foydalaning yoki aniqroq savol bering.")
# 3. Asosiy ishga tushirish qismi
if __name__ == "__main__":
    keep_alive()  # Veb-serverni yoqish
    print("Bot hozir ishga tushdi...")
    bot.infinity_polling() # Botni doimiy aloqada saqlash
