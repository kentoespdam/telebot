from datetime import datetime
from ping3 import ping
from config.conn import customConnection
from mysql.connector import Error


class PingResult:
    def __init__(self, host: str, result: str, status: bool):
        self.host = host
        self.result = result
        self.status = status

    def __str__(self):
        return f'Host: {self.host} Result: {self.result}, Status: {self.status}'

    def __repr__(self):
        return f'Host: {self.host} Result: {self.result}, Status: {self.status}'


def ping_host(name, host):
    result = ping(host)
    print(f"{datetime.now()} - {name} - {host} - {result}")
    if result != None or result == False:
        time = round(result*1000)
        return PingResult(host, f'Host *[{name}]* _{host}_ is UP ✅ with {time} ms', True)
    return PingResult(host, f'Host *[{name}]* _{host}_ is DOWN ❌', False)


def ping_db(
        host: str,
        port: str,
        username: str,
        password: str,
        database: str = None,
        name: str = None
):
    result = ""
    try:
        connection = customConnection(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        ).build()
        result = f"Result Server {name if name else host} : estabilished"
        if connection:
            connection.close()
    except Error as e:
        result = f"Error Server {name if name else host}: {e.msg}"

    return result
