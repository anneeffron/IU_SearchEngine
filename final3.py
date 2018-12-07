#! /usr/bin/env python3
import nltk,string, json, math, sys
import nltk.stem.porter as p
from collections import Counter


#------------------------------------------------
#Notes
# i used hw2 to generate the invindex.dat and docs.dat files
#using the invindex.dat I created a dictionary of all the words in the corpus and their count
#i saved this as docs.dat and references this file for the dictioary instead of calculating it all the time

#i then used the cgi to get the information from the student
#------------------------------------------------


#this function normalizes the words

def normalized(wordDict, wordCount):
    tfDict = {}
    #looping through the word dictionary associated with the webpage that holds the words and count of these words
    for word in wordDict:
        #checking to see if the word is in the query that the user typed in
        if word in cleanSteemer:
            #if it is normalize the word
            tfDict[word] = wordDict[word]/float(wordCount)
    return tfDict


#this function calculates tfidf
def tfidf(wordDict):
    total =0
    #going through each word and calcualting tfidf
    for word in wordDict:
        calculate = wordDict[word] * (1/(1+math.log(float(dfDict[word]))))
        total += calculate
    return total




#--------------------------------------------

#Main

#--------------------------------------------







#question, ask, background
#this will be a dictionary holding all the words in the corpus and the number of the times each word appeared
dfDict = {}
# #getting the user input and stripping it and making it lower case to tokenzie it
#words = "indiana"
words = sys.argv[1]
words = words.lower()
words = words.strip()
# # mode = sys.argv[1]
# # words = sys.argv[2:]
# # words = " ".join(words)®
#
# #cleaning and tokenzing the word lst
lst = []
tokenList = nltk.word_tokenize(str(words))

#
#
# #opening the stopwords
with open("stopwords.txt", "r") as file2:
    stopwords = file2.readlines()
    stop= [stopwords[i].strip() for i in range(len(stopwords))]

for token in tokenList:
    if token not in stop:
        lst.append(token.lower())
#
#  #stemming each word in the words list
stemmer = p.PorterStemmer()
stemmerWords = [stemmer.stem(word) for word in lst]

#
# #taking care of punctation in this stem list,
cleanSteemer = [word for word in stemmerWords if not [letter for letter in word if letter in string.punctuation]]

print(cleanSteemer)
#
#
# #opening the two files
try:
    with open("docs.dat","r") as file:
        urls = json.load(file)

except:
    print("docs file not found")

try:
    with open("invindex.dat", "r") as file2:
        wordDict = json.load(file2)
        for word in wordDict:
            count = 0
            wordlst = wordDict[word]
            for item in wordlst:
                count += item[1]
                dfDict[word] = count

except:
    print("invindex file not found")


try:
    with open("pageRanks.dat", "r") as file3:
        pageRank = json.load(file3)


except:
    print("pageRank file not found")

#
#
# # try:
# #     with open("words.dat", "r") as file3:
# #         dfDict = json.load(file3)
# #
# # except:
# #     print("file not found")
#
#
#
#list of all the links, titles, and tfidf ranks
tfList = []

#adding to this lst the words in the dfdict
checkLst = []
# looping through the query checking to see if each word in the query is in the dictionary
for i in range(len(cleanSteemer)):
    if cleanSteemer[i] in dfDict:
        checkLst.append(cleanSteemer[i])

#creating a set
checkLst = set(checkLst)
print(checkLst)
#
#
for url in urls:
    #creating a set
    setDoc = set(urls[url]["tokenWords"])
    #seeing the intersection of the query and the words
    most = checkLst.intersection(setDoc)
    #returning "most", here the words have to appear at least half of the checklst
    if len(most) >= len(checkLst) //2 :
        #normalizing the words in a the document
        urls[url]["tokenWords"] = normalized(urls[url]["tokenWords"], urls[url]["wCt"])
        #performing tfidf
        if urls[url]["tokenWords"]:
            tf = tfidf(urls[url]["tokenWords"])
            #making sure there is a tf rank
            if tf != 0:
                tfList.append([tf, url, urls[url]["url"], urls[url]["title"]])

#

for item in tfList:
    if pageRank.get(item[1]):
        item[0] =  float(item[1]) * float(pageRank.get(item[1]))


# #sorting the tfList
tfList = sorted(tfList, reverse=True)
#
# #creating another list that will hold just the titles and urls
# finalList = []
#
# for item in tfList:
#     #https://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20/35953321 to take care of the encoding error with title
#     item[2] = item[2].encode('ascii', 'ignore').decode('ascii')
#     #item[2] = item[2].encode('utf-8').decode('utf-8')
#     finalList.append([item[2], item[1], item[0]])
#
# #finding how many results there are
resultsCount= len(tfList)

print(resultsCount, "results founds")
# for item in tfList:
#     print(item)


#
# #if the list exists printing out a list of the top 25 results
if tfList:

    if len(tfList) >= 25:
        print("only top 25 results showing")
        for i in range(25):
            print(tfList[i])
    else:
        for item in tfList:
            print(item)






#print(pageRank)
#
