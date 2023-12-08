import logging
from telegram import Update
from config import (
    TELEGRAM_TOKEN,
    CHOOSE_DB,
    CHOOSE_SERVER,
    ECommands
)
from handlers.startHandler import start, commands
from handlers.pingHandler import (
    pingDbHandler,
    pingHandler,
    pingServerDbHandler,
    pingServerHandler
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)
from callbacks.pingCallback import selectedDb, selectedServer
from callbacks.cancelCallback import cancel
from warnings import filterwarnings
from telegram.warnings import PTBRuntimeWarning
from schedulers.pingSchedule import toThread

# enable logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
filterwarnings(
    action="ignore",
    message=r".*CallbackQueryHandler",
    category=PTBRuntimeWarning
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler(ECommands.START.value, start))
    app.add_handler(CommandHandler(ECommands.COMMANDS.value, commands))
    app.add_handler(CommandHandler(ECommands.PING.value, pingHandler))
    app.add_handler(CommandHandler(ECommands.PING_DB.value, pingDbHandler))
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler(ECommands.PING_SERVER.value, pingServerHandler),
            CommandHandler(ECommands.PING_DB_SERVER.value, pingServerDbHandler)
        ],
        states={
            CHOOSE_SERVER: [
                CallbackQueryHandler(cancel, pattern=f"^Cancel$"),
                CallbackQueryHandler(selectedServer),
            ],
            CHOOSE_DB: [
                CallbackQueryHandler(cancel, pattern=f"^Cancel$"),
                CallbackQueryHandler(selectedDb),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_handler)
    # jobs = app.job_queue
    # jobs.run_repeating(toThread, interval=30, first=5)

    print("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
