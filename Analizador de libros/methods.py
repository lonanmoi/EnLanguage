# -*- coding: utf-8 -*-
"""
Created on Sat May  2 18:25:53 2020

@author: lonan
"""
import collections
import re
import os
from termcolor import colored

import requests
import bs4
from bs4 import BeautifulSoup

from googletrans import Translator
import csv


removeVerbsWords = ["had","hadden","heb","hebt","heeft","hebben","zal","zult","zullen","zou","zouden"]


#---------------------------------- SAVING BOOKS IN LISTS---------------------------------------------------------
def getUniqueWordsFromList(list):
    tempList=[]

    for w in list:
        if w not in tempList:
            tempList.append(w)
    return tempList

def getUniqueWordsFromFile(route):
    with open(route,'r', encoding='utf8') as f:
        lines = f.readlines()
    list = []
    for l in lines:
        splitted = l.split(" ")
        for i in splitted:
            list.append(i)
        list[-1] = list[-1][:-1]

    return list

def formatWord(word):
    w = ""
    for c in word:
        if(c != "."):
            w+=c
        if(c == "\'"):
            w="0"
            break
    return w



def sortWordsFromFile(route="") -> list:
    if(route==""):
        print("Empty route")#TODO: ver si se pude usar un error propio de python aqui tipo notFilefound o algo asi
        return []

    words = re.findall(r'\w+',open (route,encoding="utf8").read().lower())
    most_common_list=collections.Counter(words).most_common()
    lista_palabras=[]


    for x in range(0,len(most_common_list)):
        lista_palabras.append((most_common_list[x])[0])


    lista_palabras=eliminateNumbersFromList(lista_palabras)


    return lista_palabras
def sortAndCountWordsFromFile(route = "") -> list:
    if(route==""):
        print("Empty route")#TODO: ver si se pude usar un error propio de python aqui tipo notFilefound o algo asi
        return []

    words = re.findall(r'\w+',open (route,encoding="utf8").read().lower())
    most_common_list=collections.Counter(words).most_common()


    return most_common_list

def sortWordsFromFileAndSave(routeOrigin="",routeSave=""):
    wordsList = sortWordsFromFile(routeOrigin)
    if(routeSave == ""):
        routeSave = routeOrigin[0:(len(routeOrigin)-4)]+"Sorted.txt"
        saveListInFile(routeSave,wordsList)
    else:
        saveListInFile(routeSave,wordsList)
def sortAndCountWordsFromFileSave(routeOrigin="",routeSave=""):
    wordsList = sortAndCountWordsFromFile(routeOrigin)
    if(routeSave == ""):
        routeSave = routeOrigin[0:(len(routeOrigin)-4)]+"SortedAndNumber.txt"
        saveListInFile(routeSave,wordsList)
    else:
        saveListInFile(routeSave,wordsList)

def saveWordsFromRouteListToFile(list):
    for route in list:
        print(route)
        sortWordsFromFileAndSave(route)
        sortAndCountWordsFromFileSave(route)



def getUniqueElementsInFileFromFile(originalRoute,removeRoute):

    originalList = sortWordsFromFile(originalRoute)
    originalList=eliminateNumbersFromList(originalList)

    removeList = sortWordsFromFile(removeRoute)
    removeList = eliminateNumbersFromList(removeList)

    return getUniqueElementsInListFromList(originalList,removeList)
def getUniqueElementsInListFromList(originalList, removeList):
    uniquesList= []
    for i in originalList:
        if i not in removeList:
            uniquesList.append(i)
    return uniquesList

def eliminateNumbersFromList(list):
    noDigitList=[]
    for c in list:
        if(c.isdigit()==False):
            noDigitList.append(c)
    return noDigitList

def saveListInFile(route,list):
    if(isinstance(list[0], tuple)):
        saveFile=open(route,'w',encoding="utf8")
        with saveFile as f:
            for line in list:
                f.write(line[0]+";"+str(line[1])+"\n")
            saveFile.close()
    else:
        saveFile=open(route,'w',encoding="utf8")
        with saveFile as f:
            for line in list:
                f.write(line+"\n")
            saveFile.close()




###
##
#TODO: Mirar que pollas hace esto
def eliminateNumbersFromListwithNumberscounted(list):
    indexesList = []
    for index,l in enumerate(list):
        x = any(map(str.isdigit, l[0]))
        if(x == True):
            indexesList.append(index)

    for i in reversed(indexesList):
        list.pop(i)

    return list

def eliminateIsolatedLettersFromListWithNumbersCounted(list):
    indexesList = []
    for index,l in enumerate(list):
        w= l[0]
        if(len(w)==1):
            indexesList.append(index)

    for i in reversed(indexesList):
        list.pop(i)

    return list







#######-------=========----------=========---------========---------=========--------##########
#######-------=========----------=========---------========---------=========--------##########
#######-------=========----------=========---------========---------=========--------##########
# ESTOS METODOS SE USAN EN DUTCHANALISIS PERO CREO QUE YA NO HACEN FALTA
#PORQUE ERAN LOS QUE USABAN METODOS CON LISTAS Y NO CON DATAFRAMES

#Return the indexes in list1 that are equal to some object of the list2
def getIndexesToEliminateRepeatetedItemsInList1FromList2(list1,list2):
    tempList=[]
    for l2 in list2:
        for i,l1 in enumerate(list1):
            if (l1 == l2):
                tempList.append(i)
    return tempList

#Return the indexes and objects in list1 that are equal to some object of the list2
def getIndexesAndObjectsToEliminateRepeatetedItemsInList1FromList2(list1,list2):
    tempList=[]
    for l2 in list2:
        for i,l1 in enumerate(list1):
            if (l1 == l2):
                tempList2 = (i,l1)
                tempList.append(tempList2)
    return tempList

def eliminateElementsFromListGivenIndexes(list,listIndex):
    for i in listIndex:
        list.pop(i)

    return list

#######-------=========----------=========---------========---------=========--------##########
#######-------=========----------=========---------========---------=========--------##########
#######-------=========----------=========---------========---------=========--------##########








#------------------------------------------ VERBS -----------------------------------------------------------
#Devuelve los tiempos verbales de un verbo
def dutchGetTensesFromVerb(name) -> list:
    if(len(name)!=0):
        res =requests.get('https://cooljugator.com/nl/'+name)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        pronouns =soup.findAll('div',class_='conjugation-cell conjugation-cell-four conjugation-cell-pronouns pronounColumn')


        if(len(pronouns) > 10):
            tenses = soup.findAll('div',class_='meta-form')

            if(len(tenses)==56):
                print("Verbo regular")
                tensesList=[]

                for w in tenses:
                    #print(w.getText())
                    tensesList.append(w.getText())

                #print("\n\n")
                lista = dutchSaveRegularVerbalTensesInLists(tensesList,name)

                return lista

            else:
                print("Verbo con distinto numero de tiempos verbales")
                tensesList=[]
                tensesList.append(name)
                tensesList.append(2)
                return tensesList

        elif(len(pronouns)<=10 and len(pronouns)!=0):
            print("Verbo irregular")
            tenses = soup.findAll('div',class_='meta-form')
            tensesList=[]
            tensesList.append(name)
            tensesList.append(0)
            for w in tenses:
                #print(w.getText())
                tensesList.append(w.getText())

            return tensesList

        else:
            print("El verbo no existe")
            return -1
    else:
        print("No hay verbo")
        return -1
def dutchGetKeyTenses(name):
    res =requests.get('https://cooljugator.com/nl/'+name)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    tenses = soup.findAll('div',class_='meta-form')

    verbsList =[]
    for w in tenses:
        splitted = w.getText().split(" ")
        if(len(splitted) > 1):
            for i in splitted:
                verbsList.append(i)
        else:
            verbsList.append(w.getText())

    if(len(verbsList) > 0 ):
        most_common_list=collections.Counter(verbsList).most_common()
        verbsList=[]

        for w in most_common_list:
            verbsList.append(w[0])

        verbsList=eliminateNumbersFromList(verbsList)
    return getUniqueElementsInListFromList(verbsList,removeVerbsWords)
def dutchGetKeyTensesFromListOfVerbs(listOfWords):
    listOfTensesList = []
    for w in listOfWords:
        words = dutchGetKeyTenses(w)
        listOfTensesList.append(words)

    return listOfTensesList
def dutchGetKeyTensesFromListOfVerbsAndSave(listOfWords,routeSave):
    listOfTensesList = dutchGetKeyTensesFromListOfVerbs(listOfWords)

    with open(routeSave,'w',encoding="utf8") as f:
        for l in listOfTensesList:
            for w in l:
                f.write(w+"\n")

#Lee los verbos del txt, obtiene los tiempos verbales y los guarda en un csv
def dutchReadVerbsFromTextAndSaveVerbalTensesInCsv(routeToRead="savedVerbs.txt",routeToSave="savedVerbsWithTense.csv"):

    #Lee todos los verbos
    print(routeToRead)
    print("\n\n\n\n")
    f = open(routeToRead,'r')
    verbsList=[]
    for l in f.readlines():
        verbsList.append(l.strip('\n'))
    f.close()
    verbsList.pop(-1)
    print(verbsList)



    #Busca los tiempos verbales de los verbos
    verbsList2=[]
    for v in verbsList:
       a= dutchGetTensesFromVerb(v)
       if(a!=-1):
           verbsList2.append(a)


    #Guarda los verbos con sus tiempos verbales en un csv
    with open(routeToSave,'w') as f:
        for v in verbsList2:
            if(v[1]==1):
                f.write(str(v[0])+",")
                f.write(str(v[1])+",")

                for i in range(2,len(v)):
                    for j in v[i]:
                        f.write((j+","))
            elif(v[1]==2):
                f.write(str(v[0])+",")
                f.write(str(v[1])+";")
            elif(v[1]==0):
                f.write(str(v[0])+",")
                f.write(str(v[1])+",")
                for i in range(2,len(v)):
                    f.write(v[i]+",")
            f.write("\n")



    #
    for x in verbsList2:
        if(len(x)>1):
            for y in x:
                print(y)
            print("\n")
#Crea un lista con todos los tiempos verbales de verbos regulares agrupados en listas de tiempos verbales
def dutchSaveRegularVerbalTensesInLists(list,infinitive=""):
    bigList=[]
    bigList.append(infinitive)
    bigList.append(1)
    i=0
    for a in range(0,9):
        tempList = []
        for a in range(0,6):
            tempList.append(list[i])
            i=i+1
        bigList.append(tempList)

    tempList=[]
    for a in range(0,2):
        tempList.append(list[i])
        i=i+1
    bigList.append(tempList)

    return bigList






def enGetKeyTenses(name):
    res =requests.get('https://conjugator.reverso.net/conjugation-english-verb-'+name+'.html')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    #Get all the concreted words from the tenses
    tenses =soup.findAll(class_='verbtxt')
    tempList=[]



    for w in tenses:
        tempList.append(w.getText())

    print("/////////////////////////////////////")
    most_common = collections.Counter(tempList)
    most_common_list=most_common.most_common()
    tempList = []

    for w in most_common_list:
        tempList.append(w[0])

    return tempList
def enGetKeyTensesFromListOfVerbs(listOfWords):
    listOfTensesList = []
    for w in listOfWords:
        words = enGetKeyTenses(w)
        listOfTensesList.append(words)

    return listOfTensesList
def enGetKeyTensesFromListOfVerbsAndSave(listOfWords,routeSave):
    listOfTensesList = enGetKeyTensesFromListOfVerbs(listOfWords)
    with open(routeSave,'w',encoding="utf8") as f:
        for l in listOfTensesList:
            for w in l:
                f.write(w+"\n")


#------------------------------------- TRANSLATIONS ----------------------------------------------------------------
# GOOGLE
def getTranslationGoogleEnNl(word=""):
    if(word != ""):
        trans = Translator()
        t = trans.translate(
            word,
            src='en' ,
            dest='nl'
        )
        return t.text
    else:
        print("Error, no hay palabra")
        return -1
def getTranslationGoogleEnEs(word=""):
    if(word != ""):
        trans = Translator()
        t = trans.translate(
            word,
            src='en' ,
            dest='es'
        )
        return t.text
    else:
        print("Error, no hay palabra")
        return -1
def getTranslationGoogleEsNl(word=""):
    if(word != ""):
        trans = Translator()
        t = trans.translate(
            word,
            src='es' ,
            dest='nl'
        )
        return t.text
    else:
        print("Error, no hay palabra")
        return -1
def getTranslationGoogleNlEn(word=""):
    if(word != ""):
        trans = Translator()
        t = trans.translate(
            word,
            src='nl' ,
            dest='en'
        )
        return t.text
    else:
        print("Error, no hay palabra")
        return -1
def getTranslationGoogleNlEs(word=""):
    if(word != ""):
        trans = Translator()
        t = trans.translate(
            word,
            src='nl' ,
            dest='es'
        )
        return t.text
    else:
        print("Error, no hay palabra")
        return -1

#GLOSBE
#Translate from Glosbe netherlands to english
def getTranslationGlosbeNlEn(word=""):
    if(word!=""):
        res =requests.get('https://glosbe.com/nl/en/'+word)
        soup = bs4.BeautifulSoup(res.content, 'html.parser')

        words =soup.findAll('strong',class_='phr')
        tempList=[]
        for w in words:
            tempList.append(w.getText())
        return tempList


    else:
        print ("No hay palabra")
        return -1

#------------------------------------------ ATRIBUTES -----------------------------------------------------


#########################
#########################
#TODO: https://m.interglot.com/nl/en/?q=boeken Nuevo metodo con est
#########################
#########################

##### De Momento no funciona
def getTranslationInterglotNlEn(word=""):
    res =requests.get('https://m.interglot.com/nl/en/?q='+word)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')

    words = soup.findAll('div',class_="hanging-indent")

    words = soup.find('div', attrs={'class': 'hanging-indent'})


    print(words)
    # for w in words:
    #     print(w.getText())




    print("")
####






#Return a list with the IPA,Gender,Type
def dutchGetAttributesFromWordGlosbe(word=""):
    res =requests.get('https://glosbe.com/nl/en/'+word)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    print(type(soup))
    #Get the main atributes
    word = soup.findAll(class_='defmetas')

    atr=word[0].getText()
    atrList =atr.split(";")
    print(atrList)




    #List with the atributes gender: ??? , Ipa: ???, type: ???
    atributesList=[]
    for i in atrList:
        #removes the first blank space of the string
        if(i[0]==' '):
            i = i[1:]
        atributesList.append(i)


    #Gets all the types from the diferent translations that the word has and takes the one that repeats the most
    types = soup.findAll(class_='gender-n-phrase')

    tempstring=""
    for t in types:
        for c in t.getText():
            if(c.isalpha() or c == ','):
                tempstring=tempstring+c
            elif(c==";"):
                tempstring=tempstring+','

        tempstring=tempstring+","


    #Removes the last ","
    tempstring = tempstring[0:-1]

    #Saves the most common word in a list
    words = re.findall(r'\w+',tempstring)
    most_common = collections.Counter(words)
    most_common_list=most_common.most_common()




    #Find the index in the list that contains the string type
    i=0
    for j in atributesList:
        for c in j:
            if(j.find("Type:") != -1):
                savedindex=i
        i=i+1

    #write in the indeix that contains type the most common type
    atributesList[savedindex]="Type: "+most_common_list[0][0]

    #removes the last string if its empty
    if(len(atributesList[-1])<3):
        atributesList.pop(-1)

    return atributesList

def getTypeFromAttributesList(list):
    index=0
    for i in list:
        if(i.find("Type: ")!=-1):
            savedindex=index

        index=index+1

    string = list[savedindex].replace("Type: ","")

    return string


#Return a list with the IPA,Gender,Type
def dutchGetAttributesFromWordGlosbe2(word=""):
    res =requests.get('https://glosbe.com/nl/en/'+word)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')



    word = soup.findAll(class_='defmetas')

    atr=word[0].getText()
    atrList =atr.split(";")
    print(atrList)

    atributesList=[]
    for i in atrList:
        #removes the first blank space of the string
        if(i[0]==' '):
            i = i[1:]
        atributesList.append(i)

    #List with the atributes gender: ??? , Ipa: ???, type: ???
    if(len(atributesList[-1])<3):
        atributesList.pop(-1)


    tempList=[]
    #Takes just de first type
    for i in atributesList:
        x=i.split(",")
        if(len(x)>2):
            tempList.append(x[0])
        else:
            tempList.append(i)



    return tempList









    ################
    #TODO:
    # Hay que cambiar cuando guarda el csv, se tiene que cambiar ; por ,
    # tambien habria que probar este diccionario
    # https://glosbe.com/nl/en/blijven


    #################



















    print('\n\n\n\n\n')








    #name="Holandés/Series/aresT1complete.txt"
    #saveWordsSortedAndNumber(name)

    # print(colored("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/",'green'))
    # #print("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
    # nombre1="libros/aGameOfThrones"
    # nombre2="VocabularioPropio"
    # provList =eliminateWordsInListFromFile(nombre1,nombre2)
    # saveListInFile("vocabularioASeleccionar/aGameOfThronesSelect.txt",provList[2])













def main():
    print(colored("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/",'green'))
    print("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
    atr = dutchGetAttributesFromWordGlosbe("boek")
    words=getTranslationGlosbeNlEn("blijven")
    print(colored("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/",'blue'))
    print(atr)
    print(words)







def main2():
    print(colored("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/",'green'))
    print("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")


    word=rootWord("doen","do"," ","verb")
    word.show()



    # a=dutchGetTensesFromVerb("doen")
    # print(a)
    # print("len: ")
    # print(len(a))




    print(colored("=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/",'blue'))








def main3():
    lista = [["hola",5],["xDD",8],["23o34",23],["i",3],["alskdn",5]]
    lista= eliminateIsolated
    print(lista)


def main4():
    # listWords = ["remember","go","come","do","eat","drink"]
    # listOfTensesList = []
    # for w in listWords:
    #     words = enGetKeyTenses(w)
    #     listOfTensesList.append(words)
    #
    #
    # with open('ingles\\otros\\dataframes exported\\english verbal tenses.txt','w',encoding="utf8") as f:
    #     for l in listOfTensesList:
    #         for w in l:
    #             f.write(w+"\n")

    print("")











if(__name__ == '__main__'):
    #print(os.getcwd())
    os.chdir(r'E:\Lonan\Programacion\python\Analizador de libros')
    main4()
    print('\n')
