import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. Kalitlarni olish
GEMINI_KEY = os.getenv("GEMINI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 2. Gemini va Botni sozlash (Eng barqaror usul)
genai.configure(api_key=GEMINI_KEY)
# 'gemini-1.5-flash' o'rniga 'gemini-pro' ishlatamiz - bu 404 bermaydi
model = genai.GenerativeModel('gemini-pro') 
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is active and running!"

# 3. Chat funksiyasi
@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Gemini-dan javob olish
        response = model.generate_content(message.text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Kechirasiz, javob topa olmadim.")
            
    except Exception as e:
        # Xatoni aniq ko'rsatish
        bot.reply_to(message, f"Xatolik: {str(e)}")

# 4. Render serveri uchun qism
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    # Flaskni alohida oqimda yoqish
    threading.Thread(target=run, daemon=True).start()
    print("Bot yoqildi...")
    # Telegramni doimiy yoqiq holatda ushlash
    bot.infinity_polling()
