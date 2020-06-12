import random
import sys
from view import View
from word import Word

class Exercise:
    def __init__(self, word):
        self.word = Word(word)
        self.question = self.word.define().option().output()
        self.symbols = ["A", "B", "C", "D"]
        self.view = View()

    def interact(self):
        self.view.sentence(self.question["definition"], 80)
        self.view.options(self.symbols, self.question["options"])

        while True:
            picked = input("Please input your choice:")

            if picked.upper() == 'Q':
                sys.exit(0)

            if picked.upper() not in self.symbols:
                continue

            choices = dict()
            for symbol, value in zip(self.symbols, self.question["options"]):
                choices[symbol] = value

            picked = choices[picked.upper()]

            if self.word.evaluate(picked) == True:
                self.view.evaluate(True)
            else:
                correct_symbol = ''
                for index in choices:
                    if choices[index] == self.question["word"]:
                        correct_symbol = index
                        break

                self.view.evaluate(False, correct_symbol)

            break


class Loop:
    def __init__(self):
        self.view = View()

    def header(self):
        self.view.clear()
        self.view.header(80)
        self.view.title("Exercise")

    def choice(self):
        with open("words.conf", encoding='utf-8') as file:
            wordlist = file.read()
            wordlist = wordlist.split("\n")
            word = random.choice(wordlist)
            return word

    def run(self):
        self.header()
        while True:
            exercise = Exercise(self.choice())
            exercise.interact()

def main():
    try:
        loop = Loop()
        loop.run()
    except Exception as error:
        print(error)

main()