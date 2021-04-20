import os
import time
from typing import Any

import MySQLdb
from MySQLdb.cursors import Cursor


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


def execute(query: Any, args: Any = None) -> Any:
    connection: MySQLdb.Connection = connect()
    cursor: Cursor = connection.cursor()

    connection.autocommit(True)
    cursor.execute(query, args)
    connection.close()

    return cursor


def exist(table: str) -> bool:
    return execute("SHOW TABLES LIKE %s", (table,)).rowcount > 0


def log(message: str):
    """Log text in console and in database

    Args:
        message (string): Text to be logged
    """

    # logging.getLogger('paperbot').error(message)
    execute("INSERT INTO log_info (`text`, `time`) VALUES (%s, %s)", (message, time.time(),))
