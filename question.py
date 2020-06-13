import sys
from view import View
from word import Word

class Question:
    def __init__(self, word):
        self.word = Word(word)
        self.question = self.word.define().option().output()
        self.symbols = ["A", "B", "C", "D"]
        self.view = View()
        self.isCorrect = False

    def cleanLog(self):
        # remove duplicated word in wrong.log
        data = ''
        with open("wrong.log", encoding="utf-8") as file:
            error_list = file.read()
            error_list = error_list.strip("\n")
            error_list = error_list.split("\n")
            error_list = list(set(error_list))
            for item in error_list:
                data = data + f"{item}\n"
        with open('wrong.log', 'w', encoding='utf-8') as file:
            file.write(data)

    def syncErrorConf(self):
        with open('wrong.log', encoding='utf-8') as file:
            data = file.read()
            with open("errors.conf", 'w', encoding='utf-8') as file:
                file.write(data)

    def interact(self):
        self.view.sentence(self.question["definition"], 80)
        self.view.options(self.symbols, self.question["options"])

        while True:
            picked = input("Please input your choice: ")

            if picked.upper() == 'Q':
                sys.exit(0)

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

                # write error word into wrong.log
                with open('wrong.log', 'r+') as file:
                    wrong_word_list = file.read()
                    if "\n" in wrong_word_list:
                        wrong_word_list = wrong_word_list.strip("\n")
                        wrong_word_list = wrong_word_list.split("\n")
                        wrong_word_list.append(self.question["word"])
                        wrong_word_list = list(set(wrong_word_list))
                    else:
                        wrong_word_list = [self.question["word"]]

                    for word in wrong_word_list:
                        if word != '':
                            file.write(f"{self.question['word']}\n")
                            break
            break

        if self.isCorrect == False:
            self.cleanLog()
            self.syncErrorConf()