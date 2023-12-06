import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler
import schedule
import time
from botmodules.pingDbHandler import pingDbHandler
from botmodules.pingDbServerHandler import pingDb, dbSelected, pingDbServerHandler
from botmodules.start import start, commands
from botmodules.pingHandler import pingHandler
from botmodules.pingServerHandler import pingServer, pingServerHandler, serverSelected
from modules.pingSchedule import job

# enable logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
load_dotenv()

# schedule.every(5).seconds.do(job)


def main():
    app = ApplicationBuilder().token(str(os.getenv("TELEGRAM_TOKEN"))).build()

    app.add_handler(CommandHandler("start", start))  # /start
    app.add_handler(CommandHandler("commands", commands))  # /commands
    app.add_handler(CommandHandler("ping", pingHandler))  # /ping
    app.add_handler(CommandHandler("pingdb", pingDbHandler))
    # app.add_handler(pingServerHandler()) # /pingserver
    # app.add_handler(pingDbServerHandler()) # /pingdbserver
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('pingserver', pingServer)],
        states={
            2: [CallbackQueryHandler(serverSelected)]
        },
        fallbacks=[CommandHandler('pingserver', pingServer)]
    ))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('pingdbserver', pingDb)],
        states={
            1: [CallbackQueryHandler(dbSelected)],
        },
        fallbacks=[CommandHandler('pingdbserver', pingDb)]
    ))

    print("Bot Starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
