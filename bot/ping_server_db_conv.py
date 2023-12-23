from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from config import (
    DB,
    CHOOSE_SERVER_DB,
    fetch_server_list,
    list_server_keyboard,
    finish_keyboard,
    PROM_QUERY
)


async def ping_server_db(update: Update, context: ContextTypes) -> int:
    servers = fetch_server_list(DB)
    reply_markup = list_server_keyboard(servers)
    await update.message.reply_text(
        "Please choose a server to ping",
        reply_markup=reply_markup
    )
    return CHOOSE_SERVER_DB


async def choose_server_db(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "cancel":
        await query.message.edit_text("Ping cancelled")
        return ConversationHandler.END
    message = get_db_status(query.data)
    await query.edit_message_text(message, reply_markup=finish_keyboard(), parse_mode="Markdown")
    return ConversationHandler.END


def get_db_status(ip):
    label_config = {"instance": ip}
    r_status = PROM_QUERY.get_current_metric_value(
        metric_name="mysql_up", label_config=label_config)
    r_version = PROM_QUERY.get_current_metric_value(
        metric_name="mysql_version_info", label_config=label_config)
    status = int(r_status[0]['value'][1])
    version = r_version[0]['metric']['version']
    if status == 1:
        return f"✅ Connection {ip} Success...```Version: {version}```"
    return f"❌ Connection {ip} Failed..."
