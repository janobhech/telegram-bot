import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import os

# --- 1. SOZLAMALAR ---
# Google AI Studiodan olgan API kalitingizni shu yerga qo'ying
GEMINI_API_KEY = "SIZNING_GEMINI_API_KALITINGIZ"

# BotFatherdan olgan Telegram tokenni shu yerga qo'ying
TELEGRAM_TOKEN = "8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA"

# AI Modelini ulash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram botni ishga tushirish
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- 2. RENDER UCHUN SERVER (Bot o'chib qolmasligi uchun) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Online va Xavfsiz ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 3. BOT BUYRUQLARI ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Bu yerda faqat sizning xabaringiz turadi
    welcome_text = (
        "Assalomu alaykum! 👋\n\n"
        "Men yuridik yordamchi AI botman. Savolingizni yozing, "
        "men O'zbekiston qonunchiligi asosida javob berishga harakat qilaman."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # AIga yuboriladigan savol
        user_query = message.text
        
        # AIga qat'iy yuridik vazifa beramiz
        prompt = f"Sen professional o'zbek yuristisan. Faqat O'zbekiston qonunlari va Lex.uz asosida javob ber: {user_query}"
        
        # AI javobi
        response = model.generate_content(prompt)
        
        # Foydalanuvchiga javobni qaytarish
        bot.reply_to(message, response.text)
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        bot.reply_to(message, "Kechirasiz, hozirda javob bera olmayman. Birozdan so'ng qayta urinib ko'ring.")

# --- 4. ISHGA TUSHIRISH ---
if __name__ == "__main__":
    keep_alive() # Serverni yoqish
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling() # Botni doimiy aloqada saqlash
