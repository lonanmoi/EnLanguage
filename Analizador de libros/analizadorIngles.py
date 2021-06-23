import requests
import bs4
import os
from bs4 import BeautifulSoup
import time

import re
import methods as me

import pandas as pd
import numpy as np

import collections
import time

WORD = "Palabra"
TOTAL_AMMOUNT = "Suma Total"
GRAMMAR_CATEGORY = "Categoria gramatical"
OXFORD  = "Oxford5000"
VOC = "Voc"


##
#Prefixes:
# o : Oxford methods. Means that the method is gonna work around Oxford vocabulary page

###########
#Estos metodos fueron improvisados para crear los dataframes. No tienen uso ahora
def ogetWords():

    #####
    #####
    # oxfordvocSplitted.txt es simplemente el archivo de la pagina web quitandole todo lo que no sea el
    # codigo que contiene las palabras a buscar
    #####
    #####

    with open('ingles\otros\oxfordvocSplitted.txt','r',encoding='utf-8') as f:
        contentlist=f.readlines()
        #contentstring = f.read()

    tempList=[]
    for i in contentlist:
        x = i.replace('data-hw="',"")
        tempList.append(x)

    tempList2=[]
    for s in tempList:
        x = s.split('"')
        tempList2.append(x[0])


    return tempList2

def ogetOxford3000():
    with open('ingles\otros\oxfordvocSplitted.txt','r',encoding='utf-8') as f:
        contentlist=f.readlines()
        #contentstring = f.read()

    tempList=[]
    for i in contentlist:
        x=i.find('data-ox3000="')
        if(x!=-1):
            y=x + len('data-ox3000="')
            tempList.append(i[y:])
        else:
            tempList.append("-1")



    tempList2=[]
    for s in tempList:
        if(s!=-1):
            x = s.split('"')
            tempList2.append(x[0])
        else:
            tempList2.append("-1")



    return tempList2

def ogetOxford5000():
    with open('ingles\otros\oxfordvocSplitted.txt','r',encoding='utf-8') as f:
        contentlist=f.readlines()
        #contentstring = f.read()

    tempList=[]
    for i in contentlist:
        x=i.find('data-ox5000="')
        if(x!=-1):
            y=x + len('data-ox5000="')
            tempList.append(i[y:])
        else:
            tempList.append("-1")



    tempList2=[]
    for s in tempList:
        if(s!=-1):
            x = s.split('"')
            tempList2.append(x[0])
        else:
            tempList2.append("-1")



    return tempList2

def ogetGrammarCategory():
    with open('ingles\otros\oxfordvocSplitted.txt','r',encoding='utf-8') as f:
        contentlist=f.readlines()
        #contentstring = f.read()

    tempList=[]
    for i in contentlist:
        x=i.find('<span class="pos">')
        if(x!=-1):
            y=x + len('<span class="pos">')
            tempList.append(i[y:])
        else:
            tempList.append("-1")



    tempList2=[]
    for s in tempList:
        if(s!=-1):
            x = s.split('</span>')
            tempList2.append(x[0])
        else:
            tempList2.append("-1")


    return tempList2

#---------------------
def insertWordCountToDataFrameUsingLists(df,listwords,name="Default name"):
    #Coge una palabra y la busca a ver si se encuentra en el dataframe
        #Si se encuentra guarda el indice y se añade el valor a la columna
        #Si no se encuentra se añade una fila con la palabra y el valor
    #Ordena la lista
    #Devuelve un nuevo dataframe

    dflist =df.values.tolist()


    #Busca la palabra dentro del data frame y guarda en la lista found:[palabra,numero de veces,indice en el dataframe]
    foundWords=[]
    notFoundWords=[]
    for k in listwords:
        w = k[0]
        #print(w)

        index=0
        check=False
        while(index<len(dflist) and check ==False):

            if(dflist[index][0] == w):
                check =True
                foundWords.append([w,k[1],index])


            index=index+1
        if(check == True):
            index=index-1
            # print("Palabra encontrada : %s en el indice: %i" %(w,index))

        else:
            # print("Palabra (%s) no encontrada"%w)
            # print("\n")
            notFoundWords.append([w,k[1],-1])

    # print("Found words: ")
    # for i in foundWords:
    #     print(i)
    # print("Not Found Words: ")
    # for j in notFoundWords:
    #     print(j)


    #Crea una lista,que sera la columna a insertar en el dataframe, de las veces que se repite el numero
    valueslist=[]
    for i in range(len(dflist)):
        valueslist.append(0)

    for i in foundWords:
        valueslist[i[2]]=i[1]

    #valueslist.insert(0,"name")

    #print

    df.insert(len(df.columns),name,valueslist,True)
#---------------------

def formatDataframe(df):
    df.loc[df[OXFORD] == "a1",VOC] = "a"
    df.loc[df[OXFORD] == "a2",VOC] = "a"
    df.loc[df[OXFORD] == "b1",VOC] = "b"
    df.loc[df[OXFORD] == "b2",VOC] = "b"
    df.loc[df[OXFORD] == "c1",VOC] = "c"
    df.loc[df[OXFORD] == "c2",VOC] = "c"


    df.loc[df[OXFORD].isnull(),OXFORD] = "None"
    df.loc[df[OXFORD] == 0,OXFORD] = "None"
    df.loc[df[OXFORD] == "-1",OXFORD] = "None"
    df.loc[df[OXFORD] == "0",OXFORD] = "None"

    df.loc[df[OXFORD] == "0",VOC] = "None"




    df.loc[df[VOC].isnull(),VOC] = "None"
    df.loc[df[VOC]== "0",VOC] = "None"


    df.loc[df[GRAMMAR_CATEGORY].isnull(),GRAMMAR_CATEGORY] = "None"
    df.loc[df[GRAMMAR_CATEGORY] == "0",GRAMMAR_CATEGORY] = "None"
    df.loc[df[GRAMMAR_CATEGORY] == 0,GRAMMAR_CATEGORY] = "None"


    df.fillna(0, inplace = True)
    return df



def insertWordCountToDataFrameFromFile(df,route,name="Default name"):
    wordList = me.sortAndCountWordsFromFile(route)
    insertWordCountToDataFrame(df,wordList,name)
def insertWordCountToDataFrame(df,listwords,name="Default name"):
    #Coge una palabra y la busca a ver si se encuentra en el dataframe
        #Si se encuentra guarda el indice y se añade el valor a la columna
        #Si no se encuentra se añade una fila con la palabra y el valor
    #Ordena la lista
    #Devuelve un nuevo dataframe

    column = df.loc[:,"Palabra"]
    indexList=[]
    wordsToInsertInRows=[]

    #Si la palabra no esta en el dataframe la guarda en WordsToInsert
    #Si la palabra esta en el data frame se guarda la palabra, el cont, y el indice donde insertarla
    for k in listwords:
        dfWord=column[column == k[0]]
        if(len(dfWord.index)==0):
            # print("Palabra (%s) no encontrada"%k[0])
            wordsToInsertInRows.append(k)
        else:
            indexList.append([k[0],k[1],dfWord.index[0]])

    #Añade la columna a la cual van a ir todos los numeros
    column2 = np.zeros(len(column))
    df.insert(len(df.columns),name,column2,True)

    #Insertar las filas
    for w in wordsToInsertInRows:
        row = []

        for i in range(len(df.axes[1])):
            row.append(np.nan)
        row[0]=w[0]
        row[-1]=w[1]

        df.loc[len(df)] = row
    #Insertar los valores de las palabras que si contenia el dataframe
    for w in indexList:
        df.iloc[w[2],-1]=w[1]

def changeVocWithKnownWordsFromFile(df,route):

    listOfWords = me.getUniqueWordsFromFile(route)

    return changeVocWithKnownWords(df,listOfWords)
def changeVocWithKnownWords(df,list):
    for w in list:
        bol = df.loc[df[WORD] == w][VOC] == "None"
        if(bol.array!= None and bol.array[0]):
            df.loc[df[WORD] == w,VOC] = "d"
    return df


def getUnknownWordsFromFile(df,route) -> list:
    listOfWords = me.getUniqueWordsFromFile(route)
    unknownList = []
    for w in listOfWords:
        row = df.loc[(df[WORD]==w)]
        if((row[VOC] == "None").all()):
            unknownList.append(w)


    return unknownList


def sortInAscendingOrder(df):
    df = df.sort_values(TOTAL_AMMOUNT, ascending=True)
    df = df.reset_index(drop=True)
    return df


def sortInDescendingOrder(df):
    df = df.sort_values(TOTAL_AMMOUNT, ascending=False)
    df = df.reset_index(drop=True)
    return df











def swap2LastColumns(df):
    indexSwap = []
    for i in range(len(df.columns)):
        indexSwap.append(i)

    x = indexSwap[-1]
    indexSwap[-1] = indexSwap[-2]
    indexSwap[-2] = x
    df = df.iloc[:,indexSwap]
    return df

def remakeTotalSum(df):
    df.fillna(0, inplace = True)
    if(df.columns[-1] == TOTAL_AMMOUNT):
        df.fillna(0, inplace = True)
        df.drop(df.columns[-1],axis=1, inplace=True)
        dfsum=df.sum(axis=1)
        df.insert(len(df.columns),TOTAL_AMMOUNT,dfsum,True)

    elif(len(df.columns) >= 2 and df.columns[-2] == TOTAL_AMMOUNT):
        df = swap2LastColumns(df)
        df = remakeTotalSum(df)
        return df
    else:
        print("The last column or the one before are not the Total ammout column")
    return df

def calculateTotalSum(df):
    df.fillna(0, inplace = True)
    if (TOTAL_AMMOUNT not in df.columns[range(len(df.columns))]):

        dfsum=df.sum(axis=1)
        df.insert(len(df.columns),TOTAL_AMMOUNT,dfsum,True)

    else:
        print("alksf")
    return df









###################################
################################
#TODO: Parece ser que las palabras que estan repetidas aparecen pero no las cuenta ningun libro

# Hacer pruebas: hacer 4 o 5 dataframes con los ordenes cambiados para ver si afecta a la hora de crear
# Nuevas palabras o lo que pollas sea
#################################
##################################







def main3():
    nlp = spacy.load("en_core_web_lg")
    print()

def main():
    #'http://webcache.googleusercontent.com/search?q=cache:https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000'
    #res =requests.get('http://webcache.googleusercontent.com/search?q=cache:https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000')
    res =requests.get('https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000')

    soup = bs4.BeautifulSoup(res.content, 'html.parser')




    words = soup.findAll('a', href=True)
    words2= soup.findAll(class_="pos")
    #words3=soup.findAll("li")


    del words[2:38]

    print(words[0].getText())

    print("\n\n\n")


    # for i in words2:
    #     temp = i.getText().split(" ")
    #     if(len(temp)>1):
    #         print(i.getText())






    with open('ingles\otros\savedWords1.txt','w') as f:
        for w in words:
            f.write(w.getText()+"\n")

    with open('ingles\otros\savedWords2.txt','w') as f:
        for w in words2:
            f.write(w.getText()+"\n")

def main2():
    #res =requests.get('https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000')
    #soup = bs4.BeautifulSoup(res.content, 'html.parser')


    # with open("ingles\\otros\\SavedOxfordVoc.txt",'r',encoding="utf8") as f:
    #     contentlist=f.readlines()


    # splitedList=[]
    # for c in contentlist:
    #     x = c.split(";")
    #     y=x[-1].replace("\n","")
    #     x[-1]=y
    #     splitedList.append(x)


    df=pd.read_csv("E:\\Lonan\\Programacion\\python\\Analizador de libros\\ingles\\otros\\dataframes exported\\newDataFrameTest.csv", delimiter=";",encoding="utf-8")
    print(df.head(15))

    #lista = [["hola",2],["above",6],["zone",8],["able",4],["about",2],["aslkd",9]]
    #insertWordCountToDataFrame(df,lista)


    print("\n\n")
    # route = "E:\\Lonan\\Programacion\\python\\Analizador de libros\\ingles\\libros\\aClashOfKings.txt"
    # lista1=bgetCounterOfWordsAndSorted(route)
    # route = "E:\\Lonan\\Programacion\\python\\Analizador de libros\\ingles\\libros\\aGameOfThrones.txt"
    # lista2=bgetCounterOfWordsAndSorted(route)


    # insertWordCountToDataFrameUsingLists(df,lista1,"A clash of kings")
    # print("1")
    # insertWordCountToDataFrameUsingLists(df,lista2,"A game of thrones")



    #df.to_csv(r'E:\\Lonan\\Programacion\\python\\Analizador de libros\\ingles\\dataframes exported\\dataframe.csv',delimiter=";")
    # names = ["aClashOfKings.txt","aClashOfKings.txt","aSTormOfSwords.txt","Hp1.txt","Hp2.txt","Hp3.txt","Hp4.txt","Hp5.txt","Hp6.txt","Hp7.txt","NameOfTheWind.txt","theSlowRegardOfSilentThings.txt","Pride and prejudice.txt"]



    # for i,n in enumerate(names):
    #     route = "E:\\Lonan\\Programacion\\python\\Analizador de libros\\ingles\\libros\\" + n
    #     list  = bgetCounterOfWordsAndSorted(route)
    #     a= n[0:len(n)-4]
    #     insertWordCountToDataFrame(df,list,a)
    #     print(i)








    route = "E:\\Lonan\\Programacion\\python\\Analizador de libros\\ingles\\libros\\aGameOfThrones.txt"
    lista1 =bgetCounterOfWordsAndSorted(route)

    insertWordCountToDataFrame(df,lista1,"aGameOfThrones")





    df.to_csv(r'E:\\Lonan\\Programacion\\python\\Analizador de libros\\ingles\\otros\\dataframes exported\\newDataFrameTest.csv',sep=";",index = False)

    print(df)




    # tempList = []
    # for i in range(10):
    #     #result = re.search('data-hw="(.*)"', content[i])
    #     tempList.append(result.group(1))

def main4():
    listOfWords=[]
    with open('ingles\\otros\\dataframes exported\\englishVerbsToLookForTenses.txt','r') as f:
        x= f.readlines()

    for w in x:
        listOfWords.append(w[:-1])

    me.enGetKeyTensesFromListOfVerbsAndSave(listOfWords,'ingles\\otros\\dataframes exported\\englishTensesSaved.txt')

def tests():
    # route = "test.txt"
    # df=pd.read_csv("ingles\otros\dataFrameforTesting.csv", delimiter=";",encoding="utf-8")
    # df = formatDataframe(df)
    #
    # df = calculateTotalSum(df)
    # print(df)
    # insertWordCountToDataFrameFromFile(df,route,"Nuevo libro")
    # df=formatDataframe(df)
    # print(df)
    # #Esto es mejor hacerlo directamente con el baseDataFrame, va a ser mas practico
    # df = remakeTotalSum(df)
    # print(df)

    ###############################################

    # route = "test.txt"
    # df=pd.read_csv("ingles\otros\dataFrameforTesting.csv", delimiter=";",encoding="utf-8")
    # df = formatDataframe(df)
    # insertWordCountToDataFrameFromFile(df,route,"Nuevo libro")
    # df = formatDataframe(df)
    # print(df)
    # print("\\\\\\\\\\\\\\\\\\\\\\\\")
    #
    #
    # df = changeVocWithKnownWordsFromFile(df,"test2.txt");
    # df = formatDataframe(df)
    # print(df)
    # unknown = getUnknownWordsFromFile(df,"test.txt")
    # print("----------------------")
    # print(unknown)
    # print("999999999")
    #
    # #df.loc[df[WORD] == "coca",VOC] = "lkasdjlasd8"
    # print(df)




    # bol = (df.loc[df[WORD] == "coca"][VOC] == "None")
    # print(type(bol.array[0]))
    # if(bol.array[0]):
    #     print("true")
    # else:
    #     print("false")







    route = "ingles/otros/dataframes exported/BaseDataframeWithNoOxford3000.csv"
    df=pd.read_csv(route, delimiter=";",encoding="utf-8")
    df =formatDataframe(df)
    #pd.set_option('display.max_columns', 500)

    print(df.head(20))
    print("////////////////////////////////")
    #print(df.iloc[:,[0,3,4,5,7,9,-1]])

    df2 =df.loc[df[VOC]=="None"]
    #print(df.loc[df[VOC]=="None"])
    print(df2.head(40))
    print(df2.loc[110,:])




    # print("0-0-0-0-0-0-0-0-0-0-0-0-0")
    # df= changeVocWithKnownWordsFromFile(df,"ingles/VocabularioPropio.txt")
    # unknown = getUnknownWordsFromFile(df,"ingles/VocabularioPropio.txt")
    #
    #
    # print(df.loc[df[VOC]=="None"])
    #
    # print(unknown)
























def mainDutch():
    df=pd.read_csv("E:\\Lonan\\Programacion\\python\\Analizador de libros\\Holandés\\dataframes exported\\newDataFrameTest.csv", delimiter=";",encoding="utf-8")
    print(df.head(15))
    print("\n\n")


    # route = "E:\\Lonan\\Programacion\\python\\Analizador de libros\\Holandés\\libros\\wael008mijn02_01.txt"
    # lista1 =bgetCounterOfWordsAndSorted(route)

    # insertWordCountToDataFrame(df,lista1,"Book 5")

    # dfsum=df.sum(axis=1)
    # df.insert(len(df.columns),"Suma Total",dfsum,True)

    df = df.sort_values("Suma Total", ascending=False)


    df.to_csv(r'E:\\Lonan\\Programacion\\python\\Analizador de libros\\Holandés\\dataframes exported\\newDataFrameTest.csv',sep=";",index = False)

    print(df)

if(__name__ == '__main__'):
    #if(__name__ == '__main__'):
    #print(os.getcwd())
    start_time=time.time()
    os.chdir(r'E:\Lonan\Programacion\python\Analizador de libros')
    tests()
    end_time=time.time()-start_time
    print("Execution time: {} seconds".format(end_time))
    print('\n')
