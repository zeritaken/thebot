import logging
import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Bonjour! Je suis un bot Telegram. Tapez /menu pour afficher le menu.")

# Define the callback function for the buttons
def button(update, context):
    query = update.callback_query
    query.answer()

    # Check which button was clicked
    if query.data == 'latest_video':
        text = 'Here is the link to the latest video on nostavideos: https://www.youtube.com/watch?v=4YRPf7FfvHA'
        context.bot.send_message(chat_id=query.message.chat_id, text=text)
    elif query.data == 'subscribe':
        text = 'Click here to subscribe to nostavideos on YouTube: https://www.youtube.com/channel/UC1q-08rtIIZ5lLxoxwZJs8Q'
        context.bot.send_message(chat_id=query.message.chat_id, text=text)

# Define the menu command
def menu(update, context):
    keyboard = [[InlineKeyboardButton("Latest Video", callback_data='latest_video')],
                [InlineKeyboardButton("Subscribe", callback_data='subscribe')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def main():
    # Get the bot token from the environment variable
    TOKEN = os.environ.get('BOT_TOKEN')

    # Create the Updater and pass it the bot token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add the menu command handler
    dp.add_handler(CommandHandler('menu', menu))
    
     # Add the start command handler
    dp.add_handler(CommandHandler('start', start))

    # Add the callback query handler
    dp.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()

