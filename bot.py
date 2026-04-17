import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. AI Sozlamalari (Geminini ulash)
genai.configure(api_key="SIZNING_GEMINI_API_KALITINGIZ")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Render server
app = Flask('')
@app.route('/')
def home(): return "Bot Online ✅"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 3. Bot Sozlamalari
TOKEN = "8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    # BU YERDA REKLAMA YO'Q, FAQAT SIZNING MATNINGIZ
    bot.reply_to(message, "Assalomu alaykum! Men yuridik AI yordamchingizman. Savolingizni yozing.")

@bot.message_handler(func=lambda message: True)
def ai_answer(message):
    try:
        response = model.generate_content(f"O'zbekiston qonunlari bo'yicha javob ber: {message.text}")
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Xatolik yuz berdi. Birozdan so'ng yozing.")
if __name__ == "__main__":
    keep_alive()  # Veb-serverni yoqish
    print("Bot hozir ishga tushdi...")
    bot.infinity_polling() # Botni doimiy aloqada saqlash
