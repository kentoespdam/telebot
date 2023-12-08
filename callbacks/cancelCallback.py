from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def cancel(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()
    await context.bot.send_message(
        chat_id=user_id,
        text='Percakapan dibatalkan.'
    )
    return ConversationHandler.END
