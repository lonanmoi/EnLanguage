import methods as me
import os
route = "test.txt"
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

wordsList = []

words = me.getUniqueWordsFromFile("ingles/VocabularioPropio.txt")
for w in words:
    wordsList.append(me.formatWord(w))
print(wordsList)
