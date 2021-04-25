import os
from typing import Any

import MySQLdb
from MySQLdb.cursors import Cursor
from pony.orm import db_session

from core.models.models import LogInfo
from utility.terminal import Terminal


class Database:
    @staticmethod
    def connect() -> MySQLdb.Connection:
        """Connect to database

        Returns:
            [type]: Connection to database
        """
        return MySQLdb.connect(
            host=os.getenv("PAPERBOT.DATABASE.HOST"),
            user=os.getenv("PAPERBOT.DATABASE.USER"),
            charset="utf8mb4",
            use_unicode=True,
            passwd=os.getenv("PAPERBOT.DATABASE.PASSWD"),
            db=os.getenv("PAPERBOT.DATABASE.DB"),
        )

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
    @db_session
    def log(message: str):
        """Log text in console and in database

        Args:
            message (string): Text to be logged
        """

        # logging.getLogger('paperbot').error(message)
        Terminal.print(message)
        LogInfo(text=message)

    @staticmethod
    def ignored_user() -> list:
        result = Database.execute("SELECT id FROM ignored_user")
        if result.rowcount > 0:
            return [int(i[0]) for i in result.fetchall()]

        return []

    @staticmethod
    def level_banned_channel() -> list:
        result = Database.execute("SELECT channel FROM level_banned_channel")
        if result.rowcount > 0:
            return [int(i[0]) for i in result.fetchall()]

        return []
