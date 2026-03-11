import os
import time
import telebot
import anthropic
from dotenv import load_dotenv
from commands import register_commands

# Load environment variables
load_dotenv()

# Replace 'TELEGRAM_BOT_TOKEN' with the token you received from BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)
try:
    bot = telebot.TeleBot(TOKEN)
    register_commands(bot)

    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        """
        Handle '/start' and '/hello' commands.

        Args:
            message (telebot.types.Message): The message object.
        """
        bot.reply_to(message, "Hello! I'm a simple Telegram bot.")

    @bot.message_handler(func=lambda msg: True)
    def echo_all(message):

    user_text = message.text

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.content[0].text
    bot.reply_to(message, answer)

    # Remove webhook to avoid conflicts with polling
    bot.delete_webhook(drop_pending_updates=True)
    bot.polling()

except Exception as e:
    print(f"CRITICAL ERROR: Failed to initialize bot with provided token. Error: {e}")
    print("The application will hang to prevent a restart loop. Please fix the TELEGRAM_BOT_TOKEN environment variable.")
    while True:
        time.sleep(3600)
