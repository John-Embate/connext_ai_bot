import logging
import os
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your API details, using environment variables for security
API_URL = f"https://flowiseai-railway-production-aab9.up.railway.app/api/v1/prediction/{os.getenv('Flowise_API_KEY')}"

# Function to send queries to your API
def query_api(question):
    payload = {"question": question}
    response = requests.post(API_URL, json=payload)
    return response.json()

# Predefined questions
premade_questions = [
    "Can we file for leave on the PH holidays?",
    "How are my leave credits calculated?",
    "In what instances would I get disqualified for a perfect attendance bonus?",
    "How does Connext calculate my taxes?",
    "How can I file for overtime in Sprout?",
    "What solutions does Connext offer?",
    "What is Connext's mission?",
    "Can you discuss with me about Connext's Company Culture?"
]

# Define command handlers
def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with a custom keyboard with predefined questions when the command /start is issued."""
    reply_keyboard = [premade_questions[i:i + 2] for i in range(0, len(premade_questions), 2)]
    update.message.reply_text(
        'Hi! Use the custom keyboard below to send a predefined question, or type your own question.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Ask me something...')
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Sends a message when the command /help is issued."""
    update.message.reply_text('You can send me a question directly, or choose from the predefined ones using the custom keyboard!')

def handle_message(update: Update, context: CallbackContext) -> None:
  """Handle the message whether it is a predefined question or a custom question."""
  question = update.message.text
  response = query_api(question)

  # Extracting the 'text' field from the response
  response_text = response.get('text', 'Sorry, there was no response.')    # Default to a placeholder if no text

  # Replace '\n' with actual new lines for Telegram message formatting
  formatted_text = response_text.replace('\\n', '\n')

  update.message.reply_text(formatted_text)

def main() -> None:
    """Start the bot."""
    updater = Updater(os.getenv('Telegram_Bot_API_KEY'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
