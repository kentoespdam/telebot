from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from config import (
    SERVER,
    CHOOSE_SERVER,
    fetch_server_list,
    list_server_keyboard,
    do_ping,
    finish_keyboard
)


async def ping_server(update: Update, context: ContextTypes) -> int:
    servers = fetch_server_list(SERVER)
    reply_markup = list_server_keyboard(servers)
    await update.message.reply_text(
        "Please choose a server to ping",
        reply_markup=reply_markup
    )
    return CHOOSE_SERVER


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
