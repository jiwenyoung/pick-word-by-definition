import sqlite3 as sqlite
import urllib.request
import json
import random
import re
import os

class Word:
    def __init__(self, word):
        self.word = word
        self.definition = []
        self.options = []

    def define(self):
        # Try to get definition from database
        isWordInDatabase = False
        with sqlite.connect('definition.db') as connection:
            cursor = connection.cursor()
            sql = "SELECT word,define from words where word=?"
            cursor.execute(sql, (self.word,))
            definition = cursor.fetchone()
            if definition == None:
                isWordInDatabase = False
            else:
                isWordInDatabase = True
                definition = definition[1]
                if "|" in definition:
                    definition = definition.split("|")
                else:
                    definition = [ definition ]
                self.definition = definition

        # If not exists in database, pull from api
        def pull():
            url = f"https://owlbot.info/api/v4/dictionary/{self.word}"
            request = urllib.request.Request(url)
            request.add_header(
                "Authorization", "Token cbd6e12dbb6b45ca586e38b4a3f9a60120594ca4")
            request.add_header(
                'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')
            with urllib.request.urlopen(request) as response:
                result = json.load(response)

                cleanr = re.compile('<.*?>')

                definition = []
                for item in result["definitions"]:
                    item['definition'] = re.sub(cleanr, '', item['definition'])
                    if item['type'] != None:
                        definition.append(f"[{item['type'].upper()}]@{item['definition']}")
                    else:
                        definition.append(f"[]@{item['definition']}")
                self.definition = definition

        if isWordInDatabase == False:
            pull()

        # write pulled definition into database
        if isWordInDatabase == False:
            with sqlite.connect('definition.db') as connection:
                definition = ''
                if len(self.definition) == 1:
                    definition = self.definition[0]
                else:
                    for item in self.definition:
                        definition += f"{item}|"
                    definition = definition.strip("|")

                sql = "insert into words (word,define) values (?,?)"
                connection.execute(sql, (self.word,definition))
                connection.commit()
        return self

    def option(self):
        pool = set()
        sources = os.listdir('source')
        for source in sources:
            with open(f"source/{source}",encoding='utf-8') as file:
                for word in file:
                    word = word.strip("")
                    word = word.strip("\n")
                    pool.add(word)

            availabe = []
            while True:
                availabe = random.sample(pool, 3)
                if '' in availabe:
                    continue
                if self.word not in availabe:
                    break

            self.options = availabe
            self.options.append(self.word)
            random.shuffle(self.options)
            self.options.append('I donot know')
        return self

    def output(self):
        question = {
            "word": self.word,
            "definition": self.definition,
            "options": self.options
        }
        return question

    def evaluate(self, picked):
        if picked == self.word:
            return True
        else:
            return False
