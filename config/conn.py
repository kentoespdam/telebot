import os
import mysql.connector
from dotenv import load_dotenv
from typing import Optional
from mysql.connector.types import ParamsSequenceOrDictType

load_dotenv()


class MySQLConnectionBuilder:
    def __init__(self, port, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def build(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        ) if self.database != None else mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )


def mainConnection():
    # Get host, user, password from environment variables
    host = os.getenv('MYSQL_HOST')
    port = os.getenv('MYSQL_PORT')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv("MYSQL_DATABASE")  # Replace with your database name
    # print(f"Connecting to {host} with user {user} and password {password}")

    # Create an instance of the MySQLConnectionBuilder
    return MySQLConnectionBuilder(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port)


def customConnection(host: str, port: str, user: str, password: str, database=None) -> MySQLConnectionBuilder:
    return MySQLConnectionBuilder(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )


def update(query, params: Optional[ParamsSequenceOrDictType] = None):
    connection = mainConnection().build()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    cursor.close()
    # connection.close()
    return True
