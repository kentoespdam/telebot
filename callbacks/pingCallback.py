from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import ETables
from handlers.pingHandler import servers
from services.serverListService import findCurrentServer
from services.pingService import ping_db, ping_host


async def selectedServer(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()
    current_server = findCurrentServer(servers, query.data, ETables.SERVER)
    await query.delete_message()
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text=f"Pinging {current_server['name']}...",
        parse_mode="Markdown"
    )
    ping_result = ping_host(current_server['host'], current_server['name'])
    await query.message.reply_text(
        ping_result.message,
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def selectedDb(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()
    print(query.data)
    current_server = findCurrentServer(servers, query.data, ETables.SERVER_DB)
    print(current_server)
    await query.delete_message()
    await context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text=f"Pinging {current_server['name']}:{current_server['port']}...",
        parse_mode="Markdown"
    )
    ping_result = ping_db(
        host=current_server['host'],
        port=current_server['port'],
        username=current_server['user'],
        password=current_server['password'],
        database=current_server['schema'],
        name=current_server['name']
    )
    await query.message.reply_text(
        ping_result.message,
        parse_mode="Markdown"
    )
    return ConversationHandler.END
