from enum import Enum
import os
from dotenv import load_dotenv
from prometheus_pandas import query
import requests

load_dotenv()

TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))

PROM_URL = str(os.getenv("PROMETHEUS_URL"))

PROM_QUERY = query.Prometheus(PROM_URL)

SET_IP, CHOOSE_SERVER = range(2)


class ECommands(Enum):
    START = "start"
    COMMANDS = "commands"
    PING = "ping"
    # PING_DB = "ping_db"
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


def fetch_server_list():
    uri = f"{PROM_URL}/api/v1/targets"
    response = requests.get(uri)
    ip_server_list = []
    for server in response.json()['data']['activeTargets']:
        if server['scrapePool'] == "linux-server" or server['scrapePool'] == "win-server":
            ip_server_list.append(server['labels']['instance'].split(":")[0])

    ip_server_list.sort()
    return ip_server_list