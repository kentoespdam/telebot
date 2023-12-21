from telegram import Update
from telegram.ext import ContextTypes
from config import ECommands

async def start_bot(update: Update, context:ContextTypes)->None:
    message="Hello, I'm a bot!,\ntype /commands for use this bot."
    await update.message.reply_text(text=message)

async def commands_bot(update: Update, context: ContextTypes):
    commands = ECommands.telegramCommands()
    await update.message.reply_text(f"Available commands: \n\t\t\t{commands}")