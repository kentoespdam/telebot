from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import (
    SET_HOST_DB,
    SET_PORT_DB,
    SET_USER_DB,
    SET_PASSWORD_DB,
)
import json

from mysql.connector import connect, Error


async def start_ping_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        if (update.message.text == "cancel"):
            return ConversationHandler.END
        if (update.message.chat.type == "group"):
            await update.message.reply_text(text="Sorry, I can't work in groups")
            return ConversationHandler.END
        await update.message.reply_text(text="Hello, I'm a bot!, \nplease input your DB *HOST* address \n\n```type *cancel* to stop conversation```", parse_mode="Markdown")
    return SET_HOST_DB


async def set_host_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        text = update.message.text
        context.user_data["host_db"] = text
        if text == "cancel":
            return ConversationHandler.END
        await update.message.reply_text(f"Please Input your DB *PORT* \n\n```type *cancel* to stop conversation```", parse_mode="Markdown")
        return SET_PORT_DB
    return ConversationHandler.END


async def set_port_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        text = update.message.text
        context.user_data["port_db"] = text
        if text == "cancel":
            return ConversationHandler.END
        await update.message.reply_text(f"Please Input your DB *USERNAME* \n\n```type *cancel* to stop conversation```", parse_mode="Markdown")
        return SET_USER_DB
    return ConversationHandler.END


async def set_user_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        text = update.message.text
        context.user_data["user_db"] = text
        if text == "cancel":
            return ConversationHandler.END
        await update.message.reply_text(f"Please Input your DB *PASSWORD* \n\n```type *cancel* to stop conversation```", parse_mode="Markdown")
        return SET_PASSWORD_DB
    return ConversationHandler.END


async def set_password_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        text = update.message.text
        context.user_data["password_db"] = text
        if text == "cancel":
            return ConversationHandler.END
        pinging = koneksi(context.user_data)
        await update.message.reply_text(text=pinging, parse_mode="Markdown")
        return ConversationHandler.END
    return ConversationHandler.END


def koneksi(data: dict) -> str:
    try:
        koneksi = connect(
            host=data["host_db"],
            port=data["port_db"],
            user=data["user_db"],
            password=data["password_db"],
        )
        return f"✅ Connection Success...```Version: {koneksi.get_server_info()}```"
    except Error as e:
        return f"Error while connecting to db: {e}"
