import logging
from telegram import Update
from telegram.ext import (
    Application,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters)
from warnings import filterwarnings
from telegram.warnings import PTBRuntimeWarning
from bot.ping_conv import start_ping, set_ip
from config import (
    SET_IP,
    SET_HOST_DB,
    SET_PORT_DB,
    SET_USER_DB,
    SET_PASSWORD_DB,
    CHOOSE_SERVER,
    CHOOSE_SERVER_DB,
    TELEGRAM_TOKEN,
    ECommands
)
from bot.start import start_bot, commands_bot
from bot.ping_server_conv import ping_server, choose_server
from bot.ping_db_conv import start_ping_db, set_host_db, set_port_db, set_user_db, set_password_db
from bot.ping_server_db_conv import ping_server_db, choose_server_db

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
    # Configures the Telegram bot application with handlers for conversation flows and commands.
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler(ECommands.PING.value, start_ping),
            CommandHandler(ECommands.PING_DB.value, start_ping_db),
        ],
        states={
            SET_IP: [
                MessageHandler(filters.TEXT & ~(
                    filters.COMMAND | filters.Regex("^cancel$")), set_ip)
            ],
            SET_HOST_DB: [
                MessageHandler(filters.TEXT & ~(
                    filters.COMMAND | filters.Regex("^cancel$")), set_host_db)
            ],
            SET_PORT_DB: [
                MessageHandler(filters.TEXT & ~(
                    filters.COMMAND | filters.Regex("^cancel$")), set_port_db)
            ],
            SET_USER_DB: [
                MessageHandler(filters.TEXT & ~(
                    filters.COMMAND | filters.Regex("^cancel$")), set_user_db)
            ],
            SET_PASSWORD_DB: [
                MessageHandler(filters.TEXT & ~(
                    filters.COMMAND | filters.Regex("^cancel$")), set_password_db)
            ]
        },
        fallbacks=[],
    )
    conv_server_handler = ConversationHandler(
        entry_points=[
            CommandHandler(ECommands.PING_SERVER.value, ping_server),
            CommandHandler(ECommands.PING_DB_SERVER.value, ping_server_db),
        ],
        states={
            CHOOSE_SERVER: [
                CallbackQueryHandler(choose_server)
            ],
            CHOOSE_SERVER_DB: [
                CallbackQueryHandler(choose_server_db)
            ]
        },
        fallbacks=[],
    )
    app.add_handler(CommandHandler(ECommands.START.value, start_bot))
    app.add_handler(CommandHandler(ECommands.COMMANDS.value, commands_bot))
    app.add_handler(conv_handler)
    app.add_handler(conv_server_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
