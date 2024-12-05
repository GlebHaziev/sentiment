import sqlite3

from sqlite3 import IntegrityError
from typing import Dict


conn = sqlite3.connect("gleb_pulse_database.db")
cursor = conn.cursor()


def _init_db():
    """Инициализирует БД"""
    with open("create_tables.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def insert(table: str, column_values: Dict):
    columns = ", ".join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    try:
        cursor.executemany(
            f"INSERT INTO {table} "
            f"({columns}) "
            f"VALUES ({placeholders})",
            values
        )
        conn.commit()
    except IntegrityError as e:
        pass


_init_db()
