from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler
)
from config import PROM_URL, CHOOSE_SERVER, fetch_server_list


def chunk_list(list, size):
    for i in range(0, len(list), size):
        yield list[i:i + size]


def list_server_keyboard(servers):
    keyboard = []
    keyboard.clear()
    for chunk in chunk_list(servers, 2):
        row = []
        for server in chunk:
            row.append(InlineKeyboardButton(server, callback_data=server))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("cancel", callback_data="cancel")])
    return InlineKeyboardMarkup(keyboard)


async def ping_server(update: Update, context: ContextTypes) -> int:
    servers = fetch_server_list()
    reply_markup = list_server_keyboard(servers)
    await update.message.reply_text(
        "Please choose a server to ping",
        reply_markup=reply_markup
    )
    return CHOOSE_SERVER


async def choose_server(update: Update, context: ContextTypes) -> None:

    return ConversationHandler.END
