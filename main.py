import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the callback function for the buttons
def button(update, context):
    query = update.callback_query
    query.answer()

    # Check which button was clicked
    if query.data == 'latest_video':
        text = 'Here is the link to the latest video on nostavideos: https://www.youtube.com/watch?v=LATEST_VIDEO_ID'
        context.bot.send_message(chat_id=query.message.chat_id, text=text)
    elif query.data == 'subscribe':
        text = 'Click here to subscribe to nostavideos on YouTube: https://www.youtube.com/channel/UC-CHANNEL_ID'
        context.bot.send_message(chat_id=query.message.chat_id, text=text)

# Define the menu command
def menu(update, context):
    keyboard = [[InlineKeyboardButton("Latest Video", callback_data='latest_video')],
                [InlineKeyboardButton("Subscribe", callback_data='subscribe')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def main():
    # Get the bot token from the environment variable
    TOKEN = 'BOT_TOKEN_HERE'

    # Create the Updater and pass it the bot token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add the menu command handler
    dp.add_handler(CommandHandler('menu', menu))

    # Add the callback query handler
    dp.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
