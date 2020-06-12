import sqlite3 as sqlite
import urllib.request
import json
import random

class Word:
    def __init__(self, word):
        self.word = word
        self.definitions = ''
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
                self.definition = definition[1]

        # If not exists in database, pull from api
        if isWordInDatabase == False:
            url = f"https://owlbot.info/api/v4/dictionary/{self.word}"
            request = urllib.request.Request(url)
            request.add_header(
                "Authorization", "Token cbd6e12dbb6b45ca586e38b4a3f9a60120594ca4")
            request.add_header(
                'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')
            with urllib.request.urlopen(request) as response:
                result = json.load(response)
                definition = result["definitions"][0]["definition"]
                self.definition = definition

        # write pulled definition into database
        if isWordInDatabase == False:
            with sqlite.connect('definition.db') as connection:
                sql = "insert into words (word,define) values (?,?)"
                connection.execute(sql, (self.word, self.definition))
                connection.commit()

        return self

    def option(self):
        with open('words.conf',encoding='utf-8') as file:
            wordlist = file.read()
            wordlist = wordlist.split("\n")
            availabe = random.sample(wordlist,3)
            self.options = availabe
            self.options.append(self.word)
            random.shuffle(self.options)
            return self

    def output(self):
        question = {
            "word": self.word,
            "definition" : self.definition,
            "options" : self.options
        }
        return question

    def evaluate(self, picked):
        if picked == self.word:
            return True
        else:
            return False
