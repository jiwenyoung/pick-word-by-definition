import os

class Wrong:
    def __init__(self,word,definition):
        self.word = word
        self.definition = definition

    def record(self):
        if os.path.isdir("wrong") == False:
            os.mkdir('wrong')

        path = f"wrong/{self.word}.txt"
        with open(path,'w',encoding='utf-8') as file:
            file.write(f"{self.word}\n")
            file.write("\n")
            for index,define in enumerate(self.definition):
                if index == len(self.definition) - 1 :
                    file.write(define)
                else:
                    file.write(f"{define}\n")

        return self