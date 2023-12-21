from telegram import Update
from telegram.ext import (
    Application, 
    ConversationHandler,
    CommandHandler, 
    MessageHandler,
    CallbackQueryHandler, 
    filters)
from bot.ping_conv import start_ping, set_ip
from config import TELEGRAM_TOKEN, SET_IP,  ECommands, CHOOSE_SERVER
from bot.start import start_bot, commands_bot
from bot.ping_server_conv import ping_server


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler(ECommands.PING.value, start_ping),
        ],
        states={
            SET_IP: [
                MessageHandler(filters.TEXT & ~(
                    filters.COMMAND | filters.Regex("^Done$")), set_ip)
            ],
        },
        fallbacks=[]
    )
    app.add_handler(CommandHandler(ECommands.START.value, start_bot))
    app.add_handler(CommandHandler(ECommands.COMMANDS.value, commands_bot))
    app.add_handler(CommandHandler(ECommands.PING_SERVER.value, ping_server))
    app.add_handler(CallbackQueryHandler(set_ip))
    app.add_handler(conv_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
