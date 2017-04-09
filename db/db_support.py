# -*- coding: utf-8 -*-
from os.path import dirname, join, normpath
import sqlite3


class DbSupport:
    @classmethod
    def create_entity_list(cls, file_name):
        conn = DbSupport.connect(file_name)
        c = conn.cursor()
        table_list = DbSupport.create_table_list(c)
        entity_list = []
        for table in table_list:
            c.execute('PRAGMA table_info(' + table + ')')
            entity_list.append((table, map(lambda row: (row[1], row[2]), c.fetchall())))

        return entity_list

    @classmethod
    def connect(cls, file_name):
        db_name = normpath(join(dirname(__file__), file_name))
        return sqlite3.connect(db_name)

    @classmethod
    def create_table_list(cls, c):
        c.execute('SELECT name FROM sqlite_master WHERE type="table"')
        return map(lambda row: row[0], c.fetchall())
