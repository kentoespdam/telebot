from services.koneksi import mainConnection
from telegram import InlineKeyboardButton
from config import ETables
import json


def selectTableQuery(table: ETables):
    if table == ETables.SERVER:
        return f'SELECT * FROM {table.value} ORDER BY host ASC'
    elif table == ETables.SERVER_DB:
        return f'SELECT sd.*, s.name FROM {table.value} sd LEFT JOIN server s ON sd.host=s.host ORDER BY sd.host ASC'


def getServerList(table: ETables):
    connection = mainConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(selectTableQuery(table))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def findCurrentServer(servers: list, query: str, table: ETables):
    if table == ETables.SERVER:
        return next((server for server in servers if server['host'] == query), None)
    elif table == ETables.SERVER_DB:
        query = json.loads(query)
        print(query)
        return next((server for server in servers if server['host'] == query['host'] and server['port'] == int(query['port'])), None)


def chunk_list(list: list, chunk_size: int):
    for i in range(0, len(list), chunk_size):
        yield list[i:i + chunk_size]


def keyboardList(servers: list, table: ETables):
    keyboard = []
    keyboard.clear()
    i = 1
    for chunks in chunk_list(servers, 2):
        row = []
        for server in chunks:
            message = ""
            callback_data = ""
            if table == ETables.SERVER:
                message = f"{i}. {server['name']}"
                callback_data = server['host']
            elif table == ETables.SERVER_DB:
                message = f"{i}. {server['name']}:{server['port']}"
                callback_data = json.dumps({
                    "host": server['host'],
                    "port": str(server['port'])
                })
            row.append(
                InlineKeyboardButton(
                    message,
                    callback_data=callback_data
                )
            )
        keyboard.append(row)
        i += 1
    return keyboard