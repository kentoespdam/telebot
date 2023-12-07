from services.encryption import encode, decode


class Server:
    def __init__(self, host: str, name: str, is_online: bool):
        self.host = host
        self.name = name
        self.is_online = is_online

    def rowToServer(row: dict):
        return Server(
            host=row['host'],
            name=row['name'],
            is_online=True if row['is_online'] else False
        )


class ServerDb:
    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
            is_online: bool,
            schema: str = None,
            name: str = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.schema = schema
        self.is_online = is_online
        self.name = name

    def rowToServerDb(row: dict):
        return ServerDb(
            host=row['host'],
            port=row['port'],
            user=row['user'],
            password=row['password'],
            is_online=True if row['is_online'] else False,
            schema=row['schema'],
            name=row['name']
        )

    def decodePassword(self):
        return decode(self.password)
