import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- 1. FLASK SERVER (Botni uyg'oq saqlash uchun) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- 2. GEMINI VA TELEGRAM SOZLAMALARI ---
# Render "Environment Variables" bo'limidan olinadi
TOKEN = os.environ.get('TOKEN')
GEMINI_KEY = os.environ.get('GOOGLE_API_KEY')

# Gemini AI ni sozlash
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    # Modelni tanlash (Gemini 1.5 Flash - tezkor va tejamkor)
    model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram Botni yaratish
bot = telebot.TeleBot(TOKEN) if TOKEN else None

# --- 3. BOT FUNKSIYALARI ---
if bot:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Salom! Men Gemini AI bilan integratsiya qilingan yuridik botman. Savolingizni yozing!")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        if not GEMINI_KEY:
            bot.reply_to(message, "Xatolik: Gemini API kaliti (GOOGLE_API_KEY) o'rnatilmagan.")
            return

        try:
            # Foydalanuvchi xabarini Gemini'ga yuboramiz
            response = model.generate_content(message.text)
            # Gemini javobini foydalanuvchiga qaytaramiz
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, "❌ Hozircha Gemini bilan bog'lanib bo'lmadi. Birozdan so'ng qayta urinib ko'ring.")
            print(f"Gemini xatosi: {e}")

# --- 4. ISHGA TUSHIRISH ---
if __name__=="__main__":
    print("Bot va Gemini integratsiyasi ishga tushmoqda...")
    keep_alive()
    if bot:
        bot.infinity_polling()
