class Clean:
    def run(self):
        words = []
        with open('words.conf',encoding='utf-8') as file:
            for word in file:
                if word != '':
                    words.append(word)

        with open('words.conf','w', encoding='utf-8') as file:
            words = list(set(words))
            for word in words:
                file.write(word)

Clean().run()