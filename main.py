import os
import telebot
import anthropic
from dotenv import load_dotenv
from commands import register_commands

# Load environment variables

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize bot and AI client

bot = telebot.TeleBot(TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# Register bot commands

register_commands(bot)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a simple Telegram AI bot.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    user_text = message.text

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[
                {"role": "user", "content": user_text}
            ]
        )

        answer = response.content[0].text
        bot.reply_to(message, answer)

    except Exception as e:
        print("AI ERROR:", e)
        bot.reply_to(message, "Ошибка при обращении к AI.")

print("Bot started")

bot.delete_webhook(drop_pending_updates=True)
bot.infinity_polling()
