import os
import telebot
import anthropic
import traceback
from dotenv import load_dotenv
from commands import register_commands

# Load environment variables

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

print("TOKEN loaded:", bool(TOKEN))
print("ANTHROPIC KEY loaded:", bool(ANTHROPIC_KEY))

# Initialize bot

bot = telebot.TeleBot(TOKEN)

# Initialize AI client

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# Register commands

register_commands(bot)

@bot.message_handler(commands=['start', 'hello'])
def start(message):
bot.reply_to(message, "Hello! I'm a simple Telegram AI bot.")

@bot.message_handler(func=lambda message: True)
def chat(message):
user_text = message.text
print("User message:", user_text)

try:
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.content[0].text
    print("Claude answer:", answer)

    bot.reply_to(message, answer)

except Exception as e:
    print("AI ERROR:")
    traceback.print_exc()
    bot.reply_to(message, f"AI ERROR:\n{str(e)}")

print("Bot started")

bot.delete_webhook(drop_pending_updates=True)
bot.infinity_polling()
