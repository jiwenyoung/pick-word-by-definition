import os
import sys

class View:
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        return self

    def header(self, width, section="Exercise"):
        def output(char="*", if_end_with_new_line=False):
            if if_end_with_new_line:
                print(f'\033[1;32m{char}\033[0m')
            else:
                print(f'\033[1;32m{char}\033[0m', end="")

        def output_text(text):
            print(f"\033[1;32m{text}\033[0m", end="")

        def line():
            for i in range(width):
                if i < width - 1:
                    output()
                else:
                    output("*", True)

        def empty_line():
            for i in range(width):
                if i == 0:
                    output()
                elif i == width - 1:
                    output("*", True)
                else:
                    output(" ")

        def empty_line_without_char(line):
            for i in range(line):
                print()

        def text(text):
            for i in range(width):
                if i == 0:
                    output()
                elif i == width - len(text):
                    output("*", True)
                    break
                elif i == int((width - len(text))/2) - 1:
                    output_text(text)
                else:
                    output(" ")

        def main():
            empty_line_without_char(2)
            line()
            empty_line()
            text("Pick correct one by definition")
            text(section)
            empty_line()
            line()
            empty_line_without_char(2)

        main()
        return self

    def title(self, text):
        print()
        print(f"\033[1;32m{text}\033[0m")
        print()
        return self

    def sentence(self, text, width):
        break_index = 0
        if '@' in text:
            data = text.split("@")
            wordtype = data[0]
            text = data[1]
            print(f"\033[1;32m{wordtype} \033[0m", end="")
        else:
            print(f"\033[1;32m[] \033[0m", end="")

        for index, char in enumerate(text):
            if index == break_index and index != 0:
                print()
                continue
            if (index % width) == 0 and index != 0:
                if char == " ":
                    print()
                    continue
                else:
                    for i in range(1, 20):
                        try:
                            if text[index + i]:
                                if text[index + i] == " ":
                                    break_index = index + i
                                    break
                        except:
                            pass
            print(char, end="")
        print()

        return self

    def options(self, symbols, choices):
        for symbol, choice in zip(symbols, choices):
            if symbol != "E":
                print(f"\033[1;32m{symbol}\033[0m.{choice}", end="    ")
            else:
                print(f"\033[1;32m{symbol}\033[0m.{choice}")
        return self

    def evaluate(self, is_right, correct=''):
        if is_right == True:
            print(f"\033[1;32mCorrect!\033[0m")
        else:
            print(f"\033[1;31mWrong! Correct one is {correct}\033[0m")
        print()
        return self

    def infomation(self,text):
        sys.stderr.write(f"\n\033[1;32m{text}\033[0m\n\n")

    def warning(self, text):
        sys.stderr.write(f"\n\033[1;31m{text}\033[0m\n\n")
