import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def start(update: Update, context: ContextTypes):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def getMe(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.from_user.to_dict()
    )

async def getKeyboard(update: Update, context: ContextTypes):
    keyboard=[
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [
            InlineKeyboardButton("Option 3", callback_data='3')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)

    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=update.message.from_user.to_dict()
    # )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

# if __name__ == '__main__':
#     app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

#     handlers = []
#     handlers.append(CommandHandler('start', start))
#     handlers.append(CommandHandler('me', getMe))
#     app.add_handlers(handlers)

#     app.run_polling()
