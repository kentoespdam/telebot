import importer_test
import datetime
from services.serverListService import getServerList
import concurrent.futures
from config import ETables
import schedule
import time
from services.pingService import ping_db

pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)


def doPingDb(server) -> None:
    print(f"{server['host']} {server['port']} {server['user']} {server['password']} {server['schema']} {server['is_online']}")
    result=ping_db(
        host=server['host'],
        port=server['port'],
        username=server['user'],
        password=server['password'],
        database=server['schema'],
        name=server['name']
    )
    if (server['host'] == result.host and server['port'] == result.port and result.status != server['is_online']):
        print("beda coeg")

def pingDbJob() -> None:
    print(f"ping db job started at {datetime.datetime.now()}")

    servers = getServerList(ETables.SERVER_DB)
    for server in servers:
        # print(server)
        pool.submit(doPingDb, server)


if __name__ == "__main__":
    pingDbJob()
    pool.shutdown(wait=True)
