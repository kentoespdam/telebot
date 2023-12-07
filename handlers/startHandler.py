from telegram import Update
from telegram.ext import ContextTypes
from config import ECommands


async def start(update: Update, context: ContextTypes):
    await update.message.reply_text("Welcome to Monitor Server Bot, use /commands to see available commands")


async def commands(update: Update, context: ContextTypes):
    commands = ECommands.telegramCommands()
    await update.message.reply_text(f"Available commands: \n\t\t\t{commands}")
