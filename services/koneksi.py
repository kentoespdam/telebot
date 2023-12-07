import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from typing import Optional, Union
from mysql.connector.cursor import ParamsSequenceOrDictType

load_dotenv()


class KoneksiBuilder:
    def __init__(self, port: int, host: str, user: str, password: str, database: str = None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def build(self) -> (PooledMySQLConnection | MySQLConnection):
        if self.database is None:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                charset='latin1',
            )

        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset='latin1',
        )


def mainConnection():
    host = os.getenv('MYSQL_HOST')
    port = os.getenv('MYSQL_PORT')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv("MYSQL_DATABASE")

    return KoneksiBuilder(
        port=port,
        host=host,
        user=user,
        password=password,
        database=database
    ).build()


def customConnection(host: str,
                     port: str,
                     user: str,
                     password: str,
                     database: str = None):
    return KoneksiBuilder(
        port=port,
        host=host,
        user=user,
        password=password,
        database=database
    ).build()


def updateTable(query: [str, bytes], params: Optional[ParamsSequenceOrDictType] = None) -> bool:
    connection = mainConnection()
    cursor = connection.cursor()
    connection.start_transaction()
    cursor.execute(query, params)
    connection.commit()
    cursor.close()
    connection.close()
    return True
