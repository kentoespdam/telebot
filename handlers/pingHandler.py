from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from services.pingService import ping_db, ping_host
from services.serverListService import getServerList, keyboardList
from config import CHOOSE_DB, CHOOSE_SERVER, ECommands, ETables

servers = []


def loadServer(table: ETables):
    servers.clear()
    for row in getServerList(table):
        servers.append(row)


async def pingHandler(update: Update, context: ContextTypes):
    if (len(context.args) == 0):
        await update.message.reply_text("Please provide host to ping \nExample: /ping google.com")
    else:
        host = context.args[0]
        result = ping_host(host)
        await update.message.reply_text(
            result.message,
            parse_mode="Markdown"
        )


async def pingDbHandler(update: Update, context: ContextTypes):
    args = context.args
    args_length = len(args)
    if (args_length == 0):
        await update.message.reply_text(f"Please provide host to ping \n\t\t\tExample: /{ECommands.PING_DB} localhost 3306 root password")
    else:
        host = args[0]
        port = args[1]
        username = args[2]
        password = args[3]
        database = args[4] if (args_length == 5) else None
        result = ping_db(host, port, username, password, database)

        await update.message.reply_text(
            result.message,
            parse_mode="Markdown"
        )


async def pingServerHandler(update: Update, context: ContextTypes) -> int:
    loadServer(ETables.SERVER)
    keyboards = keyboardList(servers, ETables.SERVER)
    reply_markup = InlineKeyboardMarkup(keyboards)
    await update.message.reply_text(
        "Choose server to ping:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return CHOOSE_SERVER


async def pingServerDbHandler(update: Update, context: ContextTypes) -> int:
    loadServer(ETables.SERVER_DB)
    keyboards = keyboardList(servers, ETables.SERVER_DB)
    reply_markup = InlineKeyboardMarkup(keyboards)
    await update.message.reply_text(
        "Choose server to ping:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return CHOOSE_DB
