from bs4 import BeautifulSoup
from collections import defaultdict
import pymongo, json, os, re, codecs
from math import log10
from Parser import parse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#connecting to mongodb"
connection = pymongo.MongoClient("ds119164.mlab.com", 19164)
db = connection["invertedindex"]
db.authenticate("vincentdang", "navajo19")
tokens = db["Tokens"]

#opening and reading bookkeeping.json to use a directory
file = open("WEBPAGES_RAW/bookkeeping.json")
filestr = file.read()
bookkeeping = json.loads(filestr)
#-------------------------------------------------------

def retrieveLinks(docIDs):
    for docID in docIDs:
        print(bookkeeping[docID])

def ranking(dList):
    orderedLinks = []
    return orderedLinks
    

def retrieveDocs(dataList):
    docIDlist = []
    if len(dataList) > 0:
        for token in dataList: #list of tokens tokens = {term, docIDs, tfidf, and df}
            docIDs = token['docIDs'] #just the docIDs
            for docID in docIDs: #iterating through a list of docIDs
                for dID, tfidf in docID.iteritems(): #iterating through docID and tfidf, print either to get value.
                    docIDlist.append(dID)
    else:
        print("Word not found")

    return docIDlist


def handleInput():
    valid = True
    try:
        while(valid):
            dataList = []
            userInput = raw_input("search or q to quit: ")
            if userInput != "q":
                userInput = word_tokenize(userInput)
                for token in userInput:
                    data = tokens.find_one({'Token': token}, {'docIDs' : ''})
                    dataList.append(data)
                docs = retrieveDocs(dataList)
                #print(docs)
                count = 1
                if len(userInput) == 1:
                    docID_results = (data['docIDs'])
                    print("------------------------------------")
                    print("Top Hits:")
                    print("------------------------------------")
                    for i in docID_results[:10]: 
                        for k in i.keys():
                            print(count)
                            print(bookkeeping[k])
                            print("------------------------------------")
                            count = count + 1

                else:
                    dupes = [x for n, x in enumerate(docs) if x in docs[:n]]
                    print("------------------------------------")
                    print("Top Hits:")
                    print("------------------------------------")
                    for i in dupes[:10]:
                        print(count)
                        print(bookkeeping[i])
                        print("------------------------------------")
                        count = count + 1

            else:
                valid = False
    except:
        print("word not found")
handleInput()
    
