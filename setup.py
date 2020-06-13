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

class Configuration:
    def create(self,filename):
        if os.path.exists(filename):
            return False
        else:
            with open(filename,'w', encoding='utf-8') as file:
                pass
            return True    

    def wordlist(self):
        filename = "words.conf"
        if self.create(filename):
            print(f"{filename} is created...")
        else:
            print(f"{filename} exists...")

    def errorlist(self):
        filename = "errors.conf"
        if self.create(filename):
            print(f"{filename} is created...")
        else:
            print(f"{filename} exists...")

    def wronglog(self):
        filename = "wrong.log"
        if self.create(filename):
            print(f"{filename} is created...")
        else:
            print(f"{filename} exists...")        


class Setup:
    def run(self):
        database = Database()
        database.create()

        configuration = Configuration()
        configuration.wordlist()
        configuration.errorlist()
        configuration.wronglog()


setup = Setup()
setup.run()


