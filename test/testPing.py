import importer

from modules.pingService import ping_host, PingResult
from config.conn import mainConnection, update
import concurrent.futures
from modules.bot import send_to_group
import asyncio

connection = mainConnection().build()
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM server")
result = cursor.fetchall()
threads = []
pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)


def result_ping(server):
    pingResult = ping_host(server['name'], server['host'])
    if pingResult.status != server['is_online']:
        update("UPDATE server SET is_online = %s WHERE host = %s ",
               (pingResult.status, server["host"]))
        asyncio.run(send_to_group(pingResult.result))
    # print(pingResult)


for row in result:
    pool.submit(result_ping, row)

pool.shutdown(wait=True)
# cursor.execute("UPDATE server SET is_online = %s WHERE is_online = %s", (False, True))
cursor.close()
connection.close()
