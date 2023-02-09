import os
import logging
from telegram import ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
)
from utils import handlers

# Ajoutez un niveau de journalisation approprié pour Heroku
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Ajoutez un nom de fichier significatif pour la persistence
persistence = PicklePersistence("conversationbot_persistence")

token = os.environ["BOT_TOKEN"]

updater = Updater(token=token, use_context=True, persistence=persistence)
dispatcher = updater.dispatcher

# Utilisez des constantes pour les états au lieu de chaînes
PROCEED, FOLLOW_TELEGRAM, FOLLOW_TWITTER, FOLLOW_YOUTUBE, SUBMIT_ADDRESS, END_CONVERSATION, LOOP, SUREWANTTO, CAPTCHASTATE = range(9)

states = {
    PROCEED: [
        MessageHandler(Filters.regex("^🚀 Join Airdrop$"), handlers.submit_details),
        handlers.cancel_handler,
    ],
    FOLLOW_TELEGRAM: [
        MessageHandler(Filters.regex("^Submit Details$"), handlers.follow_telegram),
        handlers.cancel_handler,
    ],
    FOLLOW_TWITTER: [
        MessageHandler(Filters.regex("^Done$"), handlers.follow_twitter),
        handlers.cancel_handler,
    ],
    FOLLOW_YOUTUBE: [
        MessageHandler(Filters.regex("^Done$"), handlers.follow_youtube),
        handlers.cancel_handler,
    ],
    SUBMIT_ADDRESS: [handlers.cancel_handler, MessageHandler(Filters.text, handlers.submit_address)],
    END_CONVERSATION: [
        handlers.cancel_handler,
        MessageHandler(Filters.regex("^0x[a-fA-F0-9]{40}$"), handlers.end_conversation),
    ],
    LOOP: [MessageHandler(Filters.text, handlers.loop_answer)],
    SUREWANTTO: [MessageHandler(Filters.regex("^(YES|NO)$"), handlers.sure_want_to)],
    CAPTCHASTATE: [MessageHandler(Filters.text, handlers.check_captcha)],
}

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", handlers.start)],
    states=states,
    fallbacks=[],
    name="main",
    persistent=True,
)

dispatcher.add_handler(CommandHandler("list", handlers.get_list))
dispatcher.add_handler(CommandHandler("stats", handlers.get_stats))
dispatcher.add_handler(CommandHandler("bot", handlers.set_status))
dispatcher.add_handler(conv_handler)

#Démarrez le bot
if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
