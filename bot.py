import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. FLASK SERVER (Renderda bot o'chib qolmasligi uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render avtomatik beradigan PORT yoki 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 2. KONFIGURATSIYA (Render Environment Variables dan olinadi)
TOKEN = os.environ.get('TOKEN')
GEMINI_KEY = os.environ.get('GOOGLE_API_KEY')

# Gemini AI ni ulash
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram Botni ulash
bot = telebot.TeleBot(TOKEN) if TOKEN else None

# 3. BOT BUYRUQLARI
if bot:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Salom! Men Gemini AI botman. Savolingizni yozing!")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        if not GEMINI_KEY:
            bot.reply_to(message, "Xato: API kalit o'rnatilmagan.")
            return
        
        try:
            # Gemini dan javob olish
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, "Hozircha AI javob bera olmayapti, biroz kuting.")
            print(f"Xato: {e}")

# 4. ISHGA TUSHIRISH
if __name__=="__main__":
    print("Bot ishga tushmoqda...")
    keep_alive()  # Avval serverni yoqamiz
    if bot:
        bot.infinity_polling()
