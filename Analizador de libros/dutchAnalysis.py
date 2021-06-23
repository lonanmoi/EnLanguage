# -*- coding: utf-8 -*-
"""
Created on Sat May  2 18:25:53 2020

@author: lonan
"""
import collections
import re
import os
from termcolor import colored
import methods as me



class Word:
    def __init__(self,rootWord,word="",type="",count=0):
        self.word=word
        self.rootWord=rootWord
        self.type=type
        self.count=count
        

        if(type == "verb"):
            self.type ="verb"
        else:
            self.type=""

        print()
    
    #Create a verb object
    # def createVerb(self,infinitive,regular,prensentTense,presentPerfectTense,pastTense,futureTense,conditionalMood,subjunctiveMood,
    # pastPerfectTense,futurePerfect,conditionalPerfectTense,imperative):
    #     self.type = Verb(infinitive,regular,prensentTense,presentPerfectTense,pastTense,futureTense,conditionalMood,subjunctiveMood,
    #     pastPerfectTense,futurePerfect,conditionalPerfectTense,imperative)



class rootWord:
    def __init__(self,rootWord="",enTranslationGoogle="",enTranslationGlosbe="",esTranslationGoogle="",type=""):
        self.rootWord=rootWord
        self.type=type
        self.enTranslationGoogle=enTranslationGoogle
        self.enTranslationGlosbe=enTranslationGlosbe
        self.esTranslationGoogle=esTranslationGoogle

    def show(self):
        atr=vars(self)
        for key,value in atr.items():
            print(str(key)+": "+str(value))

    def createTranslations(self):
        self.createEnTranslationGoogle()
        self.createEnTranslationGlosbe()
        self.createEsTranslationGoogle()

    def createEnTranslationGoogle(self):
        self.enTranslationGoogle = me.getTranslationGoogleNlEn(self.rootWord)

    def createEnTranslationGlosbe(self):
        self.enTranslationGlosbe = me.getTranslationGlosbeNlEn(self.rootWord)
    
    def createEsTranslationGoogle(self):
        self.esTranslationGoogle=me.getTranslationGoogleNlEs(self.rootWord)

    def setType(self):
        self.type = me.getTypeFromAttributesList(me.dutchGetAttributesFromWordGlosbe(self.rootWord))


    



class Verb(rootWord):
    #
    #1 present tense
    #2 present perfect tense
    #3 past tense
    #4 future tense
    #5 conditional mood
    #6 subjunctive mood
    #7 past perfect tense
    #8 future perfect
    #9 conditional perfect tense
    #10 imperative

    def __init__(self,infinitive):
        super().__init__(infinitive,"","","","")

    def createVerbFromInfinitive(self,infinitive):
        if(len(infinitive)>1):
            x = me.dutchGetTensesFromVerb(infinitive)
            if(x[1]== 1):
                self.createVerb(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11])
            else:
                print("Error al crear el objeto el verbo no es regular")


        else:
            print("Infinitivo vacio no se ha podido crear el objeto")

    def createVerb(self,infinitive,regular,prensentTense,presentPerfectTense,pastTense,futureTense,conditionalMood,subjunctiveMood,
    pastPerfectTense,futurePerfect,conditionalPerfectTense,imperative):
        self.infinitive=infinitive
        self.regular=regular
        self.prensentTense=prensentTense
        self.presentPerfectTense=presentPerfectTense
        self.pastTense=pastTense
        self.futureTense=futureTense
        self.conditionalMood=conditionalMood
        self.subjunctiveMood=subjunctiveMood
        self.pastPerfectTense=pastPerfectTense
        self.futurePerfect=futurePerfect
        self.conditionalPerfectTense=conditionalPerfectTense
        self.imperative=imperative






def main():
    print(colored("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/",'green'))
    print("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/") 


    word=rootWord("doen","do"," ","verb")
    word.show()
    print("\n\n")

    verb = Verb("doen")
    verb.show()
    print("\n\n\n")

    verb.createVerbFromInfinitive("doen")
    verb.createTranslations()
    verb.setType()
    print("\n\n\n\n")
    verb.show()



    # a=dutchGetTensesFromVerb("doen")
    # print(a)
    # print("len: ")
    # print(len(a))




    print(colored("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/",'blue'))
    
def main2():
    # list1 = [0,1,2,3,4,5,6,7,8,9,10,90,203,405]
    # list2= [2,7,9,405]

    # indexes = me.getIndexesToEliminateRepeatetedItemsInList1FromList2(list1,list2)

    # list3 = me.eliminateElementsFromListGivenIndexes(list1,indexes)
    # print(list3)






    #Crear la lista con solo las palabras mas comunes en holandes

    with open('Holandés\csvs\mostCommonDutchWords.csv','r') as f:
        filecontent = f.readlines()


    words=[]
    for i in filecontent:
        words.append(i.strip('\n'))

    words2=[]
    for i,w in enumerate(words):
        tempList=w.split(";")
        words2.append(tempList)

    words=[]
    for w in words2:
        words.append(w[1])
    

    
    for w in words:
        print(w)
    


    #Guardar la lista en un archivo
    with open('Holandés\csvs\mostCommonDutchWordsModified.txt','w') as f:
        for w in words:
            f.write(w+"\n")


    #Leer el segundo archivo y crear una lista
    with open("Holandés\csvs\wordsToRemove.txt",'r') as f:
        filecontent = f.readlines()
    
    words2=[]
    for i in filecontent:
        words2.append(i.strip('\n'))

    print(words2)


    indexes = me.getIndexesToEliminateRepeatetedItemsInList1FromList2(words,words2)
    indexes.sort(reverse=True)


    completeWords = me.eliminateElementsFromListGivenIndexes(words,indexes)
    print("\n\n\n\n")
    print(indexes)
    print("\n")
    for w in completeWords:
        print(w)

    














#print(os.getcwd()) 
os.chdir(r'E:\Lonan\Programacion\python\Analizador de libros')
main2()
print('\n')



















    



