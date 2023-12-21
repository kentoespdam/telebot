from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import config
from ping3 import ping


async def start_ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(text="Hello, I'm a bot!, please input your IP address")
    return config.SET_IP


async def set_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        text = update.message.text
        if text == "Done":
            return ConversationHandler.END

        await update.message.reply_text(
            text=f"*Please* wait... \n`Ping to {text}`",
            parse_mode="Markdown"
        )
        output_text = ""
        for i in range(5):
            output_text += f"Ping {text} ... "
            delay = ping(text, seq=i, unit='ms')
            if delay is None:
                output_text += "Request timed out.\n"
            else:
                output_text += f"{int(delay)} ms\n"
        message=f"""
            ```Terminal \n{output_text}```
            """
        await update.message.reply_text(text=message, parse_mode="Markdown")
        return ConversationHandler.END
    return ConversationHandler.END


async def do_ping(ip: str):
    result = ping(ip, timeout=5, unit='ms')
    return result
