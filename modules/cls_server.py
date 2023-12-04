import json


class Server:
    def __init__(self, name: str, host: str, is_online: bool):
        self.name = name
        self.host = host
        self.is_online = is_online

    def dicToClass(self, data):
        self.name = data['name']
        self.host = data['host']
        self.is_online = data['is_online']
        return self

    def __str__(self):
        return f'Name: {self.name} Host: {self.host}, Status: {self.is_online}'

    def __repr__(self):
        return f'Name: {self.name} Host: {self.host}, Status: {self.is_online}'

    def __dict__(self):
        return {
            "name": self.name,
            "host": self.host,
            "is_online": self.is_online
        }

    def __json__(self):
        return json.dumps(self.__dict__())