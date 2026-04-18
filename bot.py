import os
import telebot
import google.generativeai as genai
from flask import Flask

# 1. SETTINGS & TOKENS
# Render'dagi Environment Variables bo'limidan olinadi
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# Bot va Gemini'ni sozlash
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY, transport='rest') # Shu yerga qo'shiladi
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Render uchun kichik Flask server (Portni band qilish uchun)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot ishlamoqda..."

# 2. BOT COMMANDS
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men Gemini AI bilan ishlaydigan yuridik yordamchingizman. Savolingizni bering.")

# 3. MESSAGE HANDLING
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Foydalanuvchi savoli Gemini'ga yuboriladi
        prompt = f"O'zbekiston qonunchiligi asosida javob ber: {message.text}"
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Kechirasiz, javob topilmadi.")
            
    except Exception as e:
        # Xatoni aniq ko'rish uchun (faqat tuzatish davrida)
        bot.reply_to(message, f"Texnik xato yuz berdi: {str(e)}")

# 4. RUNNING THE BOT
if __name__=="__main__":
    # Render portini avtomatik aniqlash
    port = int(os.environ.get("PORT", 8080))
    
    # Botni alohida oqimda emas, polling rejimida ishga tushirish
    print("Bot ishga tushdi...")
    
    # Flaskni fonda yurgizish (ixtiyoriy, Render uchun)
    from threading import Thread
    def run_flask():
        app.run(host='0.0.0.0', port=port)
    
    Thread(target=run_flask).start()
    
    # Telegram polling
    bot.infinity_polling()
