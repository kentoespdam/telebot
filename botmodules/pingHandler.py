from ping3 import ping
from telegram import Update
from telegram.ext import ContextTypes


async def pingHandler(update: Update, context: ContextTypes):
    if len(context.args) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide host to ping \nExample: /ping google.com"
        )
    else:
        host = context.args[0]
        pingResult = doPing(host)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=pingResult["result"]
        )


def doPing(host: str):
    pingResult = ping(host)
    if pingResult != None:
        return {
            "host": host,
            "result": f"{host} is up ✅ with {round(pingResult*1000)} ms",
            "status": True
        }
    else:
        return {
            "host": host,
            "result": f"{host} is down ❌",
            "status": False
        }
