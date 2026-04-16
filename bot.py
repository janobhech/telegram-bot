import telebot

# BotFather bergan tokenni shu yerga qo'ying
TOKEN = '8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("⚖️ Aliment masalalari")
    item2 = telebot.types.KeyboardButton("🏠 Uy-joy nizolari")
    item3 = telebot.types.KeyboardButton("📞 Advokatga savol")
    
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Xush kelibsiz! Yuridik yordam bo'limini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "⚖️ Aliment masalalari":
        bot.send_message(message.chat.id, "Aliment bo'yicha ma'lumot: Kerakli hujjatlar... (shu yerga matn yozasiz)")
    elif message.text == "🏠 Uy-joy nizolari":
        bot.send_message(message.chat.id, "Uy-joy masalalari bo'yicha: ...")
    elif message.text == "📞 Advokatga savol":
        bot.send_message(message.chat.id, "Savolingizni yozing, tez orada javob beramiz!")

bot.polling(none_stop=True)
