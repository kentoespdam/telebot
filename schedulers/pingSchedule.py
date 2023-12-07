from services.group_bot import send_to_group
from services.pingService import ping_db, ping_host
from config import ETables
import concurrent.futures
from services.koneksi import updateTable
from services.serverListService import getServerList
import asyncio
import datetime
from classes.cls_server import Server, ServerDb

####################### ping server #########################
def doPing(row) -> None:
    server = Server.rowToServer(row)
    result = ping_host(server.host, server.name)
    if (result.status != server.is_online):
        query = "UPDATE server SET is_online = %s WHERE host = %s "
        params = (result.status, server.host)

        if updateTable(query, params):
            asyncio.run(send_to_group(result.message))


def pingServerJob() -> None:
    print(f"ping server job started at {datetime.datetime.now()}")
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    servers = getServerList(ETables.SERVER)
    for server in servers:
        pool.submit(doPing, server)
    pool.shutdown(wait=True)
####################### ping server #########################


######################## ping db ############################
def doPingDb(row) -> None:
    server = ServerDb.rowToServerDb(row)
    result = ping_db(
        host=server.host,
        port=server.port,
        username=server.user,
        password=server.password,
        database=server.schema,
        name=server.name
    )

    if (result.status != server.is_online):
        query = "UPDATE server_db SET is_online = %s WHERE host = %s AND port = %s "
        params = (result.status, server.host, server.port)

        if updateTable(query, params):
            asyncio.run(send_to_group(result.message))


def pingDbJob() -> None:
    print(f"ping db job started at {datetime.datetime.now()}")
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    servers = getServerList(ETables.SERVER_DB)
    for server in servers:
        pool.submit(doPingDb, server)
    pool.shutdown(wait=True)
######################## ping db ############################

def toThread():
    rootPool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    rootPool.submit(pingServerJob)
    rootPool.submit(pingDbJob)
    rootPool.shutdown(wait=True)
