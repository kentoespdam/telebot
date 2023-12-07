import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
SECURITY_KEY = os.getenv("SECURITY_KEY")


class ECommands(Enum):
    START = "start"
    COMMANDS = "commands"
    PING = "ping"
    PING_DB = "ping_db"
    PING_SERVER = "ping_server"
    PING_DB_SERVER = "ping_db_server"

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


class ETables(Enum):
    SERVER = "server"
    SERVER_DB = "server_db"


CHOOSE_SERVER, CHOOSE_DB = range(2)
