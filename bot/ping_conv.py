from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import SET_IP,  do_ping

async def start_ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(text="Hello, I'm a bot!, please input your IP address")
    return SET_IP


async def set_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        text = update.message.text
        if text == "Done":
            return ConversationHandler.END

        await update.message.reply_text(
            text=f"*Please* wait... \n`Ping to {text}`",
            parse_mode="Markdown"
        )
        message = do_ping(text)
        await update.message.reply_text(text=message, parse_mode="Markdown")
        return ConversationHandler.END
    return ConversationHandler.END
