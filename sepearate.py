import os
import shutil

class Seperate:
    def __init__(self):
        self.pool = []
        self.reform = []
        self.words = []

    def backup(self):
        print('BACKUP...')
        os.mkdir('source-bak')
        files = os.listdir('source')
        for item in files:
            shutil.copy(f'source/{item}',f'source-bak/{item}')

        for item in files:
            if os.path.isfile(f'source-bak/{item}'):
                os.remove(f'source/{item}')
        
        return self        

    def copy(self):
        print('COPY...')
        if os.path.exists('tmp') == False:
            os.mkdir('tmp')

        with open('tmp/words.conf','w',encoding='utf-8') as file:
            files = os.listdir('source-bak')
            print(files)
            for item in files:
                with open(f'source-bak/{item}',encoding='utf-8') as source:
                    for line in source:
                        file.write(line)

        return self

    def read(self):
        print('READ...')
        with open('tmp/words.conf', encoding='utf-8') as file:
            for line in file:
                self.pool.append(line.strip('\n'))
        return self

    def formRange(self):
        print('RANGE...')
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
        print('CUT...')
        for start,end in self.reform: 
            tmp = set()
            for i in range(start, end):
                tmp.add(self.pool[i])
            self.words.append(tmp)
        return self

    def write(self):
        print('WRITE...')
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

    def clean(self):
        if os.path.isdir('tmp'):
            files = os.listdir('tmp')
            for item in files:
                os.remove(f"tmp/{item}")
            os.removedirs('tmp')
        return self

    def run(self):
        self.backup().copy().read().formRange().cut().write().clean()

Seperate().run()