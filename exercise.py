import urllib
import random
import sys
import os
from view import View
from question import Question

class Exercise:
    def __init__(self, wordfile):
        self.view = View()
        self.done = set()
        self.wordfile = wordfile
        self.wordlist = []
        self.remove = False
        self.number = 1
        self.score = {
            "correct": 0,
            "wrong": 0
        }

    def setRemove(self,remove):
        self.remove = remove
        return self

    def choice(self):
        if len(self.wordlist) == 0:
            with open(self.wordfile, encoding='utf-8') as file:
                wordlist = file.read()
                if wordlist == '':
                    sys.exit(0)
                wordlist = wordlist.split("\n")
                
                for item in wordlist:
                    if item == '':
                        wordlist.remove(item)

                self.wordlist = list(set(wordlist))

        if len(self.wordlist) == 1:
            return None
        else:
            word = ''
            while True:
                word = random.choice(self.wordlist)
                self.wordlist.remove(word)
                if word not in self.done:
                    break
            self.done.add(word)
            return word

    def do_score(self,operation):
        if operation == 'sync':
            with open("score.log",'w', encoding='utf-8') as file:
                file.write(f"correct,{self.score['correct']}\n")
                file.write(f"wrong,{self.score['wrong']}\n")

        elif operation == 'read':
            with open('score.log',encoding='utf-8') as file:
                for line in file:
                    pair = line.split(',')
                    if pair[0] == 'correct':
                        self.score['correct'] = int(pair[1])
                    elif pair[1] == 'wrong':
                        self.score['wrong'] = int(pair[1])

    def run(self):
        errors = []
        word = ''
        while True:
            try:
                word = self.choice()
                if word not in errors:
                    exercise = object()
                    if word != '' and word != None:
                        self.do_score('sync')
                        self.do_score('read')

                        print(f"#{self.number}")
                        self.number += 1
                        exercise = Question(word, self.score, self.remove)
                        question = exercise.output()
                        if exercise.interact():
                            self.score["correct"] += 1
                        else:
                            self.score["wrong"] += 1
                    else:
                        exercise = Question('test', self.score, self.remove)
                        exercise.exit()
                else:
                    continue
            except urllib.error.HTTPError as error:
                errors.append(word)
                print(error)
                continue
            except Exception as error:
                raise error


class Util:
    def clean(self):
        """Clean temp files"""
        if os.path.exists('score.log'):
            os.remove('score.log')
        if os.path.exists("words.tmp"):
            os.remove('words.tmp')
        if os.path.exists('wordpool.tmp'):
            os.remove('wordpool.tmp')
        if os.path.exists('errors.tmp'):
            os.remove('errors.tmp')
        sys.exit(0)

    def wordfile(self,argv):
        """Decide from which file words will be read"""
        if_remove = False
        wordfile = ''
        if len(argv) == 1:
            with open("wordpool.tmp","w",encoding="utf-8") as file:
                sources = os.listdir("source")
                for source in sources:
                    with open(f"source/{source}",encoding='utf-8') as src:
                        for word in src:
                            file.write(f"{word}\n")
            wordfile = 'wordpool.tmp'
        else:
            if argv[1].lower() == 'wrong':
                with open('errors.tmp','w',encoding='utf-8') as file:
                    for filename in os.listdir('wrong'):
                        wrongword = filename.strip('.txt')
                        file.write(f"{wrongword}\n")
                wordfile = "errors.tmp"

                if len(argv) == 3:
                    if argv[2].lower() == 'remove':
                        if_remove = True
            
            elif argv[1].lower() == 'new':
                sources = os.listdir('source')
                sources.sort(key=lambda fn : os.path.getmtime(f'source/{fn}'))
                wordfile = f"source/{sources[len(sources) - 1]}"
            else:
                if argv[1].endswith(".src"):
                    wordfile = f"source/{argv[1].lower()}"
                else:
                    wordfile = f"source/{argv[1].lower()}.src"
        return (wordfile,if_remove)

#Main entry
def main():
    #if remove corrected wrong word file
    if_remove = False
    util = Util()
    wordfile,if_remove = util.wordfile(sys.argv)

    #Startup
    try:
        View().clear().header(80).title(f"Exercise on {wordfile}")
        Exercise(wordfile).setRemove(if_remove).run()
    except Exception as error:
        raise error
        print(error)
        util.clean()
        pass

main()