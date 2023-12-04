import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# import modules
from .pingService import ping_host, PingResult
from .bot import send_to_group
from config.conn import mainConnection, update
import concurrent.futures
import asyncio

def result_ping(server):
    pingResult = ping_host(server['name'], server['host'])
    if pingResult.status != server['is_online']:
        print(pingResult.result)
        update("UPDATE server SET is_online = %s WHERE host = %s ",
               (pingResult.status, server["host"]))
        asyncio.run(send_to_group(pingResult.result))


def job():
    connection = mainConnection().build()
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM server")
    result = cursor.fetchall()
    for row in result:
        pool.submit(result_ping, row)
    pool.shutdown(wait=True)
    cursor.close()
    connection.close()
