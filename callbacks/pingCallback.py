from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from config import ETables
from handlers.pingHandler import servers
from services.serverListService import findCurrentServer
from services.pingService import ping_db_obj, ping_host
from classes.cls_server import ServerDb


async def selectedServer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    current_server = findCurrentServer(servers, query.data, ETables.SERVER)
    user_id=query.message.chat.id
    await query.delete_message()
    await context.bot.send_message(
        chat_id=user_id,
        text=f"Pinging {current_server['name']}...",
        parse_mode="Markdown",
    )
    ping_result = ping_host(current_server['host'], current_server['name'])
    await context.bot.send_message(
        chat_id=user_id,
        text=ping_result.message,
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def selectedDb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    current_server = ServerDb.rowToServerDb(
        findCurrentServer(servers, query.data, ETables.SERVER_DB)
    )
    user_id=query.message.chat.id
    await query.delete_message()
    await context.bot.send_message(
        chat_id=user_id,
        text=f"Pinging {current_server.name}:{current_server.port}...",
        parse_mode="Markdown"
    )
    ping_result = ping_db_obj(current_server)
    await context.bot.send_message(
        chat_id=user_id,
        text=ping_result.message,
        parse_mode="Markdown"
    )
    return ConversationHandler.END
