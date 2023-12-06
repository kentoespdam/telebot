from config.conn import mainConnection
from telegram import InlineKeyboardButton
from enum import Enum


class ETables(Enum):
    SERVER = "server"
    SERVER_DB = "server_db"


def selectTableQuery(table: ETables):
    if table == ETables.SERVER:
        return f'SELECT * FROM {table.value} ORDER BY host ASC'
    elif table == ETables.SERVER_DB:
        return f'SELECT sd.*, s.name FROM {table.value} sd INNER JOIN server s ON sd.host=s.host ORDER BY sd.host ASC'


def getListServer(table: ETables):
    connection = mainConnection().build()
    cursor = connection.cursor(dictionary=True)
    query = selectTableQuery(table)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def findCurrentServer(servers: list, host: str):
    current_row = next(
        (item for item in servers if item['host'] == host), None)
    return current_row


def chunk_list(list: list, chunk_size: int):
    for i in range(0, len(list), chunk_size):
        yield list[i:i + chunk_size]


def keyboardList(servers: list, table: ETables):
    keyboard = []
    keyboard.clear()
    i = 1
    for button_row in chunk_list(servers, 2):
        row = []
        for button in button_row:
            message = f"{i}. {button['name']}" if table == ETables.SERVER else f"{i}. {button['name']} : {button['port']}"
            row.append(InlineKeyboardButton(
                message, callback_data=button['host']))
            i += 1
        keyboard.append(row)
    return keyboard
