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
        self.score = {
            "correct": 0,
            "wrong": 0
        }

    def choice(self):
        with open(self.wordfile, encoding='utf-8') as file:
            wordlist = file.read()
            if wordlist == '':
                sys.exit(0)
            wordlist = wordlist.split("\n")
            wordlist = list(set(wordlist))

            if (len(wordlist) == len(self.done)):
                return None
            else:
                word = ''
                while True:
                    word = random.choice(wordlist)
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
        while True:
            word = self.choice()
            if word != '' and word != None:
                self.do_score('sync')
                self.do_score('read')
                exercise = Question(word, self.score)
                question = exercise.output()
                if question["definition"] == None:
                    continue
                else:
                    if exercise.interact():
                        self.score["correct"] += 1
                    else:
                        self.score["wrong"] += 1
            else:
                total = self.score["correct"] + self.score["wrong"]
                correct = self.score["correct"]
                wrong = self.score["wrong"]
                self.view.infomation(f"Total {total} questions, correct {correct}, wrong {wrong}")
                sys.exit(0)

def main():
    #Decide from which file words will be read
    wordfile = ''
    if len(sys.argv) == 1:
        with open("wordpool.tmp","w",encoding="utf-8") as file:
            sources = os.listdir("source")
            for source in sources:
                with open(f"source/{source}",encoding='utf-8') as src:
                    for word in src:
                        file.write(f"{word}\n")
        wordfile = 'wordpool.tmp'
    else:
        if sys.argv[1].lower() == 'wrong':
            wordfile = "errors.conf"
        elif sys.argv[1].lower() == 'new':
            sources = os.listdir('source')
            sources.sort(key=lambda fn : os.path.getmtime(f'source/{fn}'))
            wordfile = f"source/{sources[len(sources) - 1]}"
        else:
            if sys.argv[1].endswith(".src"):
                wordfile = f"source/{sys.argv[1].lower()}"
            else:
                wordfile = f"source/{sys.argv[1].lower()}.src"

    #write words into tmp file
    words = []
    with open(wordfile, encoding='utf-8') as file:
        for line in file:
            word = line.strip(" ")
            word = word.strip("\n")
            words.append(word)
    with open('words.tmp','w',encoding='utf-8') as file:
        for word in words:
            file.write(f"{word}\n")
    del words    

    #Startup
    try:
        View().clear().header(80).title(f"Exercise on {wordfile}")
        Exercise(wordfile).run()
    except Exception as error:
        Exercise(wordfile).run()
        pass

main()