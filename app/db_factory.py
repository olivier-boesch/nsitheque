"""
Interface de dev/prod DB pour SQLITE3/MariaDb

"""

from app.app_secrets import DB_PARAMS
import mysql.connector
import sqlite3

# ------------------------------ QUERIES

# ------------------------------ DB OBJECT

# are we in dev mode ?
try:
    from dev import __dev__
except ImportError:
    __dev__ = False

class DbInterface:
    def __init__(self):
        self.con = None
        self.connect()

    def connect(self):
        self.con = mysql.connector.connect(**DB_PARAMS)

    def make_sql_select(self, request, *args):
        if not self.con.is_connected():
            self.connect()
        with self.con.cursor(dictionary=True) as cur:
            if args:
                cur.execute(request.format(*args))
            else:
                cur.execute(request)
            data = cur.fetchall()
        self.con.commit()
        return data

    def make_sql_update(self, request, **kwargs):
        if not self.con.is_connected():
            self.connect()
        with self.con.cursor() as cur:
            cur.execute(request.format(**kwargs))
        self.con.commit()


class DevDbInterface(DbInterface):
    def __init__(self, base):
        self.base = base
        super().__init__()

    def connect(self):
        self.con = sqlite3.connect(self.base)
        self.con.row_factory = self.dict_factory

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def make_sql_select(self, request, *args):
        with self.con.cursor() as cur:
            if args:
                cur.execute(request.format(*args))
            else:
                cur.execute(request)
            data = cur.fetchall()
        self.con.commit()
        return data

    def make_sql_update(self, request, **kwargs):
        with self.con.cursor() as cur:
            cur.execute(request.format(**kwargs))
        self.con.commit()


def create_db_object(dev_mode=False):
    if dev_mode:
        return DevDbInterface('db.sqlite')
    return DbInterface()