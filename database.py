import sys
import os
import sqlite3 as sqlite

class Database:
    def create(self):
        with sqlite.connect('definition.db') as connection:
            sqls = []
            sqls.append("""CREATE TABLE words (
                word TEXT NOT NULL,
                define TEXT NOT NULL
            )""")
            for index, sql in enumerate(sqls):
                connection.execute(sql)

            print("Database Setup Finished...")
            connection.commit()
            return self

database = Database()
database.create()

