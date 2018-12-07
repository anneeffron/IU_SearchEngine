#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 00:07:52 2018

@author: ayeffron
"""

import nltk,string,os, json,sys, time, re, tools
import nltk.stem.porter as pm
from bs4 import BeautifulSoup
from collections import Counter
import multiprocessing as mp

datDict = {}
#https://github.com/keras-team/keras/issues/665
sys.setrecursionlimit(10000000)

with open("stopwords.txt", "r") as file3:
    stopwords = file3.readlines()
stop= [stopwords[i].strip() for i in range(len(stopwords))]
home = os.getcwd()
os.chdir("IU-folder")



with open("index.dat", "r") as file2:
    datFile = file2.readlines()
    datFile = [datFile[i].strip().split("\t") for i in range(len(datFile))]
    
for item in datFile:
    datDict[item[0]] = {"url": item[1], "wCt": 0, "title":"", "tokenWords":{}}



def get_text(num):
    print("going", num)
 

    with open("index-"+num+".html","r") as file2:
        contents = file2.read()
    soup = BeautifulSoup(contents, 'html.parser')


    title = soup.title.string

    title = tools.fixTitle(str(title))
    #print("title",title)


    #title = title[0:50]

    #
    text = soup.find_all(text=True)


    clean_text = ""

    for i in range(len(text)):
        text[i] = text[i].strip()
        text[i] = text[i].lower()

        clean_text += text[i]

    #print(len(clean_text))

    #print("clean_text",len(clean_text))
    #print("Whats going on")



    words= []

    tokenList = nltk.word_tokenize(clean_text)
    #print(len(tokenList))


    wordCount = len(tokenList)
    #print("word count",wordCount)




    for token in tokenList:
        if token not in stop:
            words.append(token)

    #print("Please work")

    #return (num,words,title)
    stemmer = pm.PorterStemmer()
    stemmerWords = [stemmer.stem(word) for word in words]
    cleanSteemer = [word for word in stemmerWords if not [letter for letter in word if letter in string.punctuation]]

    #print("cleanstemmer",len(cleanSteemer))

    return (num, title, wordCount, cleanSteemer)

        


nums =[]
for item in datDict:
    nums.append(item)
nums1= nums[0:50]
nums2 = nums[50:100]
nums3 = nums[100:150]
nums4 = nums[150:200]





#https://stackoverflow.com/questions/10797484/how-to-retrieve-multiple-values-returned-of-a-function-called-through-multiproce
if __name__ == "__main__":
    number_of_processes = 40
    results = mp.Pool(number_of_processes).map(get_text, nums)
    #outputs = [result[0] for result in results]
    # pf = "".join(outputs)
    #print("the length",results)
    print(len(results))

infoDict = {}

for item in results:
    datDict[item[0]]["title"] = item[1]
    datDict[item[0]]["wCt"] = item[2]
    #datDict[item[0]]["tokenWords"] = item[3]
    docWords = Counter(item[3])
    datDict[item[0]]["tokenWords"] = docWords
    for word in docWords:
        if word not in infoDict:
            infoDict[word] = [[str(item[0]), docWords.get(word)]]
        else:
            infoDict[word].append([str(item[0]), docWords.get(word)])



print(datDict)
os.chdir(home)
with open("docs.dat", 'w') as file:
    file.write(json.dumps(datDict))
with open('invindex.dat', 'w') as file:
    file.write(json.dumps(infoDict))



    # pool = mp.Pool(4)
    # for num in nums:
    #     results = pool.map(get_text, num )
    #     pool.close()
    #     pool.join()
    # for a in results:
    #     print(a)














