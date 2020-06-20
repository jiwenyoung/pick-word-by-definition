import os

class Wrong:
    def __init__(self,word,definition):
        self.word = word
        self.definition = definition
        self.path = f"wrong/{self.word}.txt" 

    def record(self):
        if os.path.isdir("wrong") == False:
            os.mkdir('wrong')

        path = self.path
        with open(path,'w',encoding='utf-8') as file:
            file.write(f"{self.word}\n")
            file.write("\n")
            for index,define in enumerate(self.definition):
                define = define.replace("@"," ")
                if index == len(self.definition) - 1 :
                    file.write(define)
                else:
                    file.write(f"{define}\n")
        return self

    def remove(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        return self