import logging
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Bonjour! Je suis un bot d'airdrop. Envoyez /airdrop pour recevoir votre jeton gratuit.")

def airdrop(update, context):
    update.message.reply_text("Félicitations! Vous avez reçu votre jeton gratuit.")

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    token = os.environ.get("BOT_TOKEN")

    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("airdrop", airdrop))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
