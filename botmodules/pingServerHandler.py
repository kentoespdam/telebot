from telegram import InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler
from modules.listServerBuilder import ETables, keyboardList, getListServer, findCurrentServer
from modules.pingService import ping_host

servers = []
current_server = {}

CHOOSE_SERVER = range(1)


def loadServer():
    list = getListServer(ETables.SERVER)
    for row in list:
        servers.append(row)


async def pingServer(update: Update, context: ContextTypes):
    loadServer()
    keyboards = keyboardList(servers, ETables.SERVER)
    reply_markup = InlineKeyboardMarkup(keyboards)
    await update.message.reply_text(
        "Please choose Server:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return 2


async def serverSelected(update: Update, context: ContextTypes):
    query = update.callback_query
    current_server = findCurrentServer(servers, query.data)
    await query.answer()

    await query.delete_message()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Pinging {current_server['name']} ...",
        parse_mode="Markdown"
    )

    pingResult = ping_host(current_server['name'], current_server['host'])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=pingResult.result,
        parse_mode="Markdown"
    )


async def endPingServer(update: Update, context: ContextTypes):
    pingResult = ping_host(current_server['name'], current_server['host'])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=pingResult.result,
        parse_mode="Markdown"
    )


def pingServerHandler():
    return ConversationHandler(
        entry_points=[CommandHandler('pingserver', pingServer)],
        states={
            CHOOSE_SERVER: [CallbackQueryHandler(serverSelected)]
        },
        fallbacks=[CommandHandler('pingserver', pingServer)]
    )
    # return [
    #     CommandHandler('pingserver', pingServer),
    #     CallbackQueryHandler(serverSelected)
    # ]
