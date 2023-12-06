from ast import pattern
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler
from modules.listServerBuilder import ETables, keyboardList, getListServer, findCurrentServer
from modules.pingService import ping_db
from modules.encryption import decrypt

CHOOSE_DB = range(1)

servers = []
current_server = {}


def loadServer():
    servers.clear()
    list = getListServer(ETables.SERVER_DB)
    for row in list:
        servers.append(row)


async def pingDb(update: Update, context: ContextTypes):
    loadServer()
    keyboards = keyboardList(servers, ETables.SERVER_DB)
    reply_markup = InlineKeyboardMarkup(keyboards)
    await update.message.reply_text(
        "Please choose Server:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return 1


async def dbSelected(update: Update, context: ContextTypes):
    query = update.callback_query
    current_server = findCurrentServer(servers, query.data)
    await query.answer()

    await query.delete_message()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Pinging {current_server['name']} ...",
        parse_mode="Markdown"
    )

    pingResult = ping_db(
        host=current_server['host'],
        port=current_server['port'],
        username=current_server['user'],
        password=current_server['password'],
        database=current_server['schema'],
        name=current_server['name']
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=pingResult,
        parse_mode="Markdown"
    )


def pingDbServerHandler():
    return ConversationHandler(
        entry_points=[CommandHandler('pingdbserver', pingDb)],
        states={
            CHOOSE_DB: [CallbackQueryHandler(dbSelected)]
        },
        fallbacks=[CommandHandler('pingdbserver', pingDb)]
    )
