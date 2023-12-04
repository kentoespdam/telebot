from typing import Dict
from telegram import Update
from telegram.ext import (
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters
)
from config.conn import customConnection

SET_HOST, SET_PORT, SET_USERNAME, SET_PASSWORD, DONE = range(5)


def dbData(db_data: Dict[str, str]) -> str:
    data = [f"{key}-{value}" for key, value in db_data.items()]
    return "\n".join(data).join(["\n", "\n"])


async def setHost(update: Update, context: ContextTypes):
    await update.message.reply_text(
        text="Please type database host:"
    )

    return SET_PORT


async def setPort(update: Update, context: ContextTypes):
    query=update.callback_query
    host = update.message.text
    context.user_data['host'] = host
    await query.edit_message_text(
        text=f"Please type database port:",
    )
    return SET_USERNAME


async def setUsername(update: Update, context: ContextTypes):
    port = update.message.text
    context.user_data['port'] = port
    await update.message.reply_text(
        text=f"Please type database username:",
    )
    return SET_PASSWORD


async def setPassword(update: Update, context: ContextTypes):
    username = update.message.text
    context.user_data['username'] = username
    await update.message.reply_text(
        text=f"Please type database password:",
    )
    return DONE


async def done(update: Update, context: ContextTypes):
    password = update.message.text
    context.user_data['password'] = password
    print(context.user_data)
    await update.message.reply_text(
        text=f"Please type database name:",
    )
    return ConversationHandler.END


def pingDbHandler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('pingdb', setHost)],
        states={
            SET_PORT: [CallbackQueryHandler(setPort)],
            SET_USERNAME: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), setUsername)],
            SET_PASSWORD: [MessageHandler(filters.TEXT & ~(
                filters.COMMAND | filters.Regex("^Done$")), setPassword)],
            DONE: [MessageHandler(filters.TEXT & ~(
                filters.COMMAND | filters.Regex("^Done$")), done)]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)]
    )
