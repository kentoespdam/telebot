import importer
from modules.cls_server import Server
import numpy as np
from enum import Enum

serverSet = set()

server1 = Server("Server 1", "192.168.1.1", True)
server2 = Server("Server 2", "192.168.1.1", True)
server3 = Server("Server 1", "192.168.1.1", True)
server4 = Server("Server 4", "192.168.1.4", True)
server5 = Server("Server 5", "192.168.1.5", True)
server6 = Server("Server 6", "192.168.1.6", True)

arr=[server1, server2, server3, server4]

slices=np.array_split(arr, 2)

print(type(arr))
print(type(slices))
print(slices[0])

class Table(Enum):
    SERVER = "server"
    SERVER_DB = "server_db"

print(Table.SERVER.value)