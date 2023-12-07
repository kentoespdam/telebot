from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Percakapan dibatalkan.')
    return ConversationHandler.END