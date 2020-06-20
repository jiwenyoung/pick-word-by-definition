import sys
import os
from view import View
from word import Word
from wrong import Wrong


class Question:
    def __init__(self, word, score):
        self.word = Word(word)
        self.question = self.word.define().option().output()
        self.symbols = ["A", "B", "C", "D"]
        self.view = View()
        self.isCorrect = False
        self.score = score

    def output(self):
        return self.question

    def exit(self):
        total = self.score["correct"] + self.score["wrong"]
        correct = self.score["correct"]
        wrong = self.score["wrong"]
        self.view.infomation(
            f"Total {total} questions, correct {correct}, wrong {wrong}")

        if os.path.exists('score.log'):
            os.remove('score.log')
        if os.path.exists("words.tmp"):
            os.remove('words.tmp')
        if os.path.exists('wordpool.tmp'):
            os.remove('wordpool.tmp')
        if os.path.exists('errors.tmp'):
            os.remove('errors.tmp')
            
        sys.exit(0)

    def interact(self):
        try:
            for element in self.question["definition"]:
                self.view.sentence(element, 80)
            self.view.options(self.symbols, self.question["options"])

            while True:
                picked = input("Please input your choice: ")

                if picked.upper() == 'Q':
                    self.exit()

                if picked.upper() not in self.symbols:
                    continue

                choices = dict()
                for symbol, value in zip(self.symbols, self.question["options"]):
                    choices[symbol] = value

                picked = choices[picked.upper()]

                if self.word.evaluate(picked) == True:
                    self.isCorrect = True
                    self.view.evaluate(True)
                else:
                    correct_symbol = ''
                    for index in choices:
                        if choices[index] == self.question["word"]:
                            correct_symbol = index
                            break

                    self.view.evaluate(False, correct_symbol)

                    # Record Error Word in wrong directory
                    wrong = Wrong(
                        self.question['word'], 
                        self.question['definition']
                    ) 
                    wrong.record()
                break

            return self.isCorrect

        except KeyboardInterrupt as error:
            self.exit()
        except Exception as error:
            raise error
