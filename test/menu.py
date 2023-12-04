import os
from dotenv import load_dotenv
from telegram.ext import (Application, Updater, CommandHandler, CallbackQueryHandler)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update)

load_dotenv()

async def start(bot, update):
    await bot.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())

async def main_menu(bot, update):
    await bot.callback_query.message.edit_text(main_menu_message(), reply_markup=main_menu_keyboard())

async def first_menu(bot, update):
    await bot.callback_query.message.edit_text(first_menu_message(), reply_markup=first_menu_keyboard())

async def second_menu(bot, update):
    await bot.callback_query.message.edit_text(second_menu_message(), reply_markup=second_menu_keyboard())

async def first_submenu(bot, update):
    pass

async def second_submenu(bot, update):
    pass

async def error(update, context):
    print(f'Update {update} caused error {context.error}')

############################ Keyboards ############################
async def main_menu_keyboard():
    keyboard=[
        [InlineKeyboardButton("Menu 1", callback_data='m1')],
        [InlineKeyboardButton("Menu 2", callback_data='m2')],
        [InlineKeyboardButton("Menu 3", callback_data='m3')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def first_menu_keyboard():
    keyboard=[
        [InlineKeyboardButton("Submenu 1-1", callback_data='m1_1')],
        [InlineKeyboardButton("Submenu 1-2", callback_data='m1_2')],
        [InlineKeyboardButton("Main menu", callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def second_menu_keyboard():
    keyboard=[
        [InlineKeyboardButton("Submenu 2-1", callback_data='m2_1')],
        [InlineKeyboardButton("Submenu 2-2", callback_data='m2_2')],
        [InlineKeyboardButton("Main menu", callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

############################ Messages ############################
async def main_menu_message():
    return 'Choose the option in main menu:'

async def first_menu_message():
    return 'Choose the submenu in first menu:'

async def second_menu_message():
    return 'Choose the submenu in second menu:'

############################ Handlers ############################
# updater=Updater(bot=os.getenv("TELEGRAM_TOKEN"), use_context=True)
# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
# updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
# updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
# updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_1'))
# updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_1'))
# updater.dispatcher.add_error_handler(error)

# updater.start_polling()

application=Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
application.add_handler(CommandHandler('start', start))
application.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
application.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
application.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
application.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_1'))
application.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_1'))
application.add_error_handler(error)

application.run_polling(allowed_updates=Update.ALL_TYPES)
