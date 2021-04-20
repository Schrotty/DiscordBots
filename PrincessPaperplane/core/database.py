import os
import time
from typing import Any

import MySQLdb
from MySQLdb.cursors import Cursor


class Database:
    def __init__(self):
        pass

    @staticmethod
    def connect() -> MySQLdb.Connection:
        """Connect to database

        Returns:
            [type]: Connection to database
        """
        return MySQLdb.connect(host=os.getenv("PAPERBOT.DATABASE.HOST"),
                               user=os.getenv("PAPERBOT.DATABASE.USER"),
                               charset="utf8mb4",
                               use_unicode=True,
                               passwd=os.getenv("PAPERBOT.DATABASE.PASSWD"),
                               db=os.getenv("PAPERBOT.DATABASE.DB"))

    @staticmethod
    def execute(query: Any, args: Any = None) -> Any:
        connection: MySQLdb.Connection = Database.connect()
        cursor: Cursor = connection.cursor()

        connection.autocommit(True)
        cursor.execute(query, args)
        connection.close()

        return cursor

    @staticmethod
    def exist(table: str) -> bool:
        return Database.execute("SHOW TABLES LIKE %s", (table,)).rowcount > 0

    @staticmethod
    def log(message: str):
        """Log text in console and in database

        Args:
            message (string): Text to be logged
        """

        # logging.getLogger('paperbot').error(message)
        Database.execute("INSERT INTO log_info (`text`, `time`) VALUES (%s, %s)", (message, time.time(),))

    @staticmethod
    def ignored_user() -> list:
        result = Database.execute('SELECT id FROM ignored_user')
        if result.rowcount > 0:
            return [int(i[0]) for i in result.fetchall()]

        return []

    @staticmethod
    def level_banned_channel() -> list:
        result = Database.execute('SELECT channel FROM level_banned_channel')
        if result.rowcount > 0:
            return [int(i[0]) for i in result.fetchall()]

        return []
