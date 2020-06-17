import threading
import urllib.request
import json
import re
import sqlite3 as sqlite
from queue import Queue

errors = Queue()

class Flush(threading.Thread):
    def __init__(self,word):
        threading.Thread.__init__(self)
        self.word = word
        self.definition = ''

    def pull(self):
        try:
            url = f"https://owlbot.info/api/v4/dictionary/{self.word}"
            request = urllib.request.Request(url)
            request.add_header("Authorization", "Token cbd6e12dbb6b45ca586e38b4a3f9a60120594ca4")
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')
            with urllib.request.urlopen(request) as response:
                result = json.load(response)
                definition = result["definitions"][0]["definition"]
                cleanr = re.compile('<.*?>')
                definition = re.sub(cleanr, '', definition)
                self.definition = definition
                print(f"pulling {self.word}")
                return self
        except Exception as error:
            print(self.word)
            errors.put(self.word)
            print(error)
            return self

    def save(self):    
        with sqlite.connect('definition.db') as connection:
    
            isWordInDatabase = False
            cursor = connection.cursor()
            sql = "SELECT word,define from words where word=?"
            cursor.execute(sql, (self.word,))
            definition = cursor.fetchone()
            if definition == None:
                isWordInDatabase = False
            else:
                isWordInDatabase = True

            if isWordInDatabase == False:
                sql = "insert into words (word,define) values (?,?)"
                connection.execute(sql, (self.word, self.definition))
                connection.commit()
                print(f"saving {self.word}")        
        return self

    def run(self):
        self.pull().save()

class Program:
    def remove(self,result):
        words = []
        with open('words.conf', encoding='utf-8') as file:
            for word in file:
                words.append(word)

        exists = []
        for word in words:
            if word not in result:
                exists.append(word)

        with open("words.conf",'w',encoding='utf-8') as file:
            for word in exists:
                file.write(f"{word}")
        

    def main(self):
        with open('words.conf', encoding='utf-8') as file:
            tasks = []
            for word in file:
                task = Flush(word)
                task.start()
                tasks.append(task)

            for task in tasks:
                task.join()

            result = []
            #print("ERRORS***************************")
            for i in range(errors.qsize()):
                result.append( errors.get() )

            self.remove(result)

Program().main()
