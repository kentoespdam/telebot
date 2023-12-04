# import logging
# from telegram import Update
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from botmodules.pingHandler import pingHandler

load_dotenv()
from botmodules.start import button, getKeyboard, start, getMe
from botmodules.serverHandler import serverHandler


def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    handlers = []
    handlers.append(CommandHandler('start', start))
    handlers.append(CommandHandler('me', getMe))
    handlers.append(CommandHandler("ping", pingHandler))
    # handlers.append(CommandHandler('keyboard', getKeyboard))
    # handlers.append(CallbackQueryHandler(button))
    handlers.append(serverHandler())
    app.add_handlers(handlers)
    # app.add_handler(CommandHandler('keyboard', getKeyboard))
    # app.add_handler(CallbackQueryHandler(button))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
