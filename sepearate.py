import os

class Seperate:
    def __init__(self):
        self.pool = []
        self.reform = []
        self.words = []

    def read(self):
        with open('words.conf', encoding='utf-8') as file:
            for line in file:
                self.pool.append(line.strip('\n'))
        return self

    def formRange(self):
        length = len(self.pool)
        for i in range(length):
            if i != 0 and i % 50 == 0:
                end = i - 1
                start = i - 50
                self.reform.append((start,end))

        if length % 50 != 0:
            start = self.reform[len(self.reform) - 1][1]
            end = length - 1
            self.reform.append((start,end))

        return self
    
    def cut(self):
        for start,end in self.reform: 
            tmp = set()
            for i in range(start, end):
                tmp.add(self.pool[i])
            self.words.append(tmp)
        return self

    def write(self):
        if os.path.isdir("source") == False:
            os.mkdir("source")

        key = 1
        for chunk in self.words:
            name = f"source/{str(key).zfill(3)}.src"
            key = key + 1
            with open(name,'w',encoding='utf-8') as file:
                for word in chunk:
                    file.write(f"{word}\n")
        return self

    def run(self):
        self.read().formRange().cut().write()


Seperate().run()