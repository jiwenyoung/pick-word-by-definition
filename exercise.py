import random
import sys
from view import View
from question import Question

class Exercise:
    def __init__(self,wordfile):
        self.view = View()
        self.done = set()
        self.wordfile = wordfile

    def header(self):
        self.view.clear()
        self.view.header(80)
        self.view.title("Exercise")

    def choice(self):
        with open(self.wordfile, encoding='utf-8') as file:
            wordlist = file.read()
            if wordlist == '':
                sys.exit(0)
            wordlist = wordlist.split("\n")
            wordlist = list(set(wordlist))

            if (len(wordlist) == len(self.done)):
                sys.exit(0)
            else:
                word = ''
                while True:
                    word = random.choice(wordlist)
                    if word not in self.done:
                        break
                self.done.add(word)
                return word

    def run(self):
        self.header()
        while True:
            word = self.choice()
            if word != '':
                exercise = Question(word)
                exercise.interact()
            else:
                sys.exit(0)

def main():
    try:
        wordfile = ''
        if len(sys.argv) == 1:
            wordfile = "words.conf"
        else:
            if sys.argv[1].lower() == 'wrong':
                wordfile = "errors.conf"

        exercise = Exercise(wordfile)
        exercise.run()
    except Exception as error:
        raise error
        print(error)
        pass

main()
