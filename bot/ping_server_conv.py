from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from config import SERVER, fetch_server_list, do_ping, finish_keyboard


def chunk_list(list, size):
    for i in range(0, len(list), size):
        yield list[i:i + size]


def list_server_keyboard(servers):
    keyboard = []
    keyboard.clear()
    if (len(servers) > 0):
        for chunk in chunk_list(servers, 2):
            row = []
            for server in chunk:
                row.append(InlineKeyboardButton(server, callback_data=server))
            keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🚫 cancel", callback_data="cancel")])
    return InlineKeyboardMarkup(keyboard)


async def ping_server(update: Update, context: ContextTypes) -> None:
    servers = fetch_server_list(SERVER)
    reply_markup = list_server_keyboard(servers)
    await update.message.reply_text(
        "Please choose a server to ping",
        reply_markup=reply_markup
    )


async def choose_server(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "cancel":
        await query.message.edit_text("Ping cancelled")
        return ConversationHandler.END
    ip = query.data
    message = do_ping(ip)
    await query.edit_message_text(message, reply_markup=finish_keyboard(), parse_mode="Markdown")

    return ConversationHandler.END
