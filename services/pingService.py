from ping3 import ping
from .koneksi import customConnection
from mysql.connector import Error
from services.encryption import decode
from classes.cls_server import ServerDb


class PingResponse:
    def __init__(self, host: str, message: str, status: bool, port: int = None):
        self.host = host
        self.status = status
        self.message = message
        self.status = status
        self.port = port

    def __str__(self):
        return f"{self.host} {self.port} {self.status} {self.message} "

    def __dict__(self):
        return {
            "host": self.host,
            "status": self.status,
            "message": self.message,
            "port": self.port
        }


def ping_host(host: str, name: str = None) -> PingResponse:
    i = 0
    result = ping(host, timeout=5, unit='s')
    while result == None and i < 3:
        result = ping(host, timeout=5)
        i += 1
    if result != None:
        time = round(result*1000, 2)
        message = f"✅ Pinging *{name if name else host}* is UP with {time} ms"
        return PingResponse(host=host, message=message, status=True)
    message = f"❌ Pinging *{name if name else host}* is Down request Timeout more than 15 seconds"
    return PingResponse(host=host, message=message, status=False)


def ping_db_obj(server: ServerDb):
    response = PingResponse(
        host=server.host,
        message="",
        status=False,
        port=server.port
    )
    try:
        connection = customConnection(
            host=server.host,
            port=server.port,
            user=server.user,
            password=decode(server.password),
            database=server.schema
        )
        if connection.is_connected():
            result = f"✅ Pinging {server.name if server.name else server.host}:{server.port} Connected"
            response = PingResponse(
                host=server.host, message=result, status=True, port=server.port)
    except Error as e:
        result = f"❌ Pinging {server.name if server.name else server.host} Error while connecting to MySQL using Connector/Python \n{e}"
        response = PingResponse(
            host=server.host, message=result, status=False, port=server.port)
    finally:
        if connection.is_connected():
            connection.close()
    return response


def ping_db(
        host: str,
        port: int,
        username: str,
        password: str,
        database: str = None,
        name: str = None
):
    response = PingResponse(host=host, message="", status=False, port=port)
    try:
        connection = customConnection(
            host=host,
            port=port,
            user=username,
            password=decode(password),
            database=database
        )
        if connection.is_connected():
            result = f"✅ Pinging {name if name else host}:{port} Connected"
            response = PingResponse(
                host=host, message=result, status=True, port=port)
    except Error as e:
        result = f"❌ Pinging {name if name else host} Error while connecting to MySQL using Connector/Python \n{e}"
        response = PingResponse(
            host=host, message=result, status=False, port=port)
    finally:
        if connection.is_connected():
            connection.close()
    return response
