from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from botmodules.pingDbHandler import pingDbHandler
from config.conn import customConnection
from mysql.connector import Error

load_dotenv()

async def start(update: Update, context: ContextTypes):
    args=context.args
    if(len(args) == 0):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide host to ping \nExample: /pingdb localhost 3306 root password"
        )
    else:
        host = args[0]
        port = args[1]
        username = args[2]
        password = args[3]
        serverInfo = ""
        try:
            connection=customConnection(host, port, username, password).build()
            serverInfo = f"{connection.get_server_info()} estabilished"
        except Error as e:
            serverInfo = f"Error: {e.msg}"
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=serverInfo
        )

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler('pingdb', start))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()