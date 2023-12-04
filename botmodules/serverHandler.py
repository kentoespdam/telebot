from config.conn import mainConnection, update
from modules.cls_server import Server
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler
)
from telegram import CallbackQuery, InlineKeyboardButton, Update, InlineKeyboardMarkup
import json
from modules.pingService import ping_host

# Stages
CHOOSE_SERVER, CHOOSE_ACTION = range(2)
# Callback data

servers = []


def getServerList() -> None:
    connection = mainConnection().build()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM server ORDER BY host ASC')
    result = cursor.fetchall()
    servers.clear()
    for row in result:
        servers.append(row)


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    getServerList()

    reply_markup = await keyboardList()

    await update.message.reply_text(
        "Please choose Server:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return CHOOSE_SERVER


async def keyboardList():
    keyboard = []
    urut = 0
    for row in servers:
        col = []
        for i in range(2):
            urut += 1
            message = f"{urut}: {row['name']}"
            json_string = json.dumps({
                "name": row['name'],
                "host": row['host'],
            })
            col.append(
                InlineKeyboardButton(
                    message, callback_data=json_string)
            )
        keyboard.append(col)
    return InlineKeyboardMarkup(keyboard)


async def selectServer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    json_data = json.loads(query.data)
    keyboard = [
        [
            InlineKeyboardButton("ping", callback_data=json.dumps(
                {"host": json_data["host"], "action": "ping"})),
            InlineKeyboardButton("pingdb", callback_data=json.dumps(
                {"host": json_data["host"], "action": "pingdb"})),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_text(
        text=f"Selected Server: \n\t\t{json_data.get('name')}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return CHOOSE_ACTION


async def selectAction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    current_server = findCurrentServer(query)
    result = result_ping(current_server)
    await query.answer()
    await query.edit_message_text(
        text=result,
        parse_mode="Markdown"
    )


def findCurrentServer(query: CallbackQuery) -> Server:
    json_data = json.loads(query.data)
    current_row = next(
        (item for item in servers if item["host"] == json_data['host']), None)
    return Server(
        current_row['name'], current_row['host'], current_row['is_online'])


def result_ping(server: Server) -> str:
    pingResult = ping_host(server.name, server.host)
    if pingResult.status != server.is_online:
        update("UPDATE server SET is_online = %s WHERE host = %s ",
               (pingResult.status, server["host"]))
    return pingResult.result


def serverHandler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('list', list)],
        states={
            CHOOSE_SERVER: [CallbackQueryHandler(selectServer)],
            CHOOSE_ACTION: [CallbackQueryHandler(selectAction)]
        },
        fallbacks=[CommandHandler('list', list)],
    )
