from telegram import Update
from telegram.ext import ContextTypes

from modules.pingService import ping_db


async def pingDbHandler(update: Update, context: ContextTypes) -> None:
    args = context.args
    if (len(args) == 0):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide host to ping \nExample: /pingdb localhost 3306 root password"
        )
    else:
        host = args[0]
        port = args[1]
        username = args[2]
        password = args[3]
        database = args[4] if len(args) == 5 else None
        serverInfo = ping_db(host, port, username, password, database)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=serverInfo
        )
