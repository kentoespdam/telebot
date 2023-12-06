from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv

load_dotenv()


async def start(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to Monitor Server Bot, use /commands to see available commands"
    )


async def commands(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Available commands: \n/pingdb \n/pingserver \n/commands"
    )
