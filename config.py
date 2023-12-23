from enum import Enum
import os
from dotenv import load_dotenv
from prometheus_pandas import query
import requests
from ping3 import ping
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))

PROM_URL = str(os.getenv("PROMETHEUS_URL"))

PROM_QUERY = query.Prometheus(PROM_URL)

SET_IP, SET_HOST_DB, SET_PORT_DB, SET_USER_DB, SET_PASSWORD_DB = range(5)

SERVER, DB = range(2)


class ECommands(Enum):
    START = "start"
    COMMANDS = "commands"
    PING = "ping"
    PING_DB = "ping_db"
    PING_SERVER = "ping_server"
    # PING_DB_SERVER = "ping_db_server"

    def commandList():
        commands = []
        for command in ECommands:
            commands.append(command.value)
        return commands

    def telegramCommands():
        return "\n\t\t\t".join(
            list(
                map(
                    lambda command: "/" + command,
                    ECommands.commandList()
                )
            )
        )


def fetch_server_list(find: SERVER | DB):
    uri = f"{PROM_URL}/api/v1/targets"
    response = requests.get(uri)
    ip_server_list = []
    for server in response.json()['data']['activeTargets']:
        if find == SERVER:
            if server['scrapePool'] == "linux-server" or server['scrapePool'] == "win-server":
                ip_server_list.append(
                    server['labels']['instance'].split(":")[0])
        else:
            if server['scrapePool'] == "mysql" or server['scrapePool'] == "mariadb":
                ip_server_list.append(
                    server['labels']['instance'].split(":")[0])

    ip_server_list.sort()
    return ip_server_list


def do_ping(ip: str) -> str:
    output_text = ""
    for i in range(5):
        output_text += f"Ping {ip} ... "
        delay = ping(ip, seq=i, unit='ms')
        if delay is None:
            output_text += "Request timed out.\n"
        else:
            output_text += f"{int(delay)} ms\n"
    return f"""
        ```Terminal \n{output_text}```
        """


def finish_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Finish ", callback_data="finish")]
    ])
