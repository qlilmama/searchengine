from bs4 import BeautifulSoup
from collections import defaultdict
import pymongo, json,re, codecs
from math import log10
from Parser import parse
import math
from nltk.corpus import stopwords, words
import os
#connecting to mongodb"
connection = pymongo.MongoClient("ds119164.mlab.com", 19164)
db = connection["invertedindex"]
db.authenticate("vincentdang", "navajo19")
tokens = db["Tokens"]
bookkeeping = json.load(open('./WEBPAGES_RAW/bookkeeping.json'))
root = "./WEBPAGES_RAW"


#NOTE:
# Term - Document Frequency (how many documents it appears in) - [DocumentID (Where its located like folder 0, file 2), term frequency(how many times it occurs)]
# Example: Irvine 2 [0/2 ,5]

#InvertedIndex = {term: {'docID': {'0/2':1,'0/1':2,'0/3':3}, 'df':3}}

stop_words = set(stopwords.words('english'))
special_terms = set()

special_terms = ['irvine', 'mondego']

def upload(term, docIDs, df):

    idx = {
        'Token': term,
        'docIDs': docIDs,
        'df': len(docIDs)-1,
        }
    tokens.insert_one(idx)

def createIndex(term):
    docIDs = ([{}])
    df = 0
    for root, dirs, files in os.walk("./WEBPAGES_RAW"):
        for name in files:
            if not name.endswith('.json') and not name.endswith('.tsv') and not name.endswith('.DS_Store'): #to filter out .json and .tsv file
                index = {}
                document = os.path.join(root,name)
                file = open(document)
                text = parse(file)
                doc_id = document.replace('./WEBPAGES_RAW/', '') #creates the documentID
                if term in text and doc_id is not '.DS_Store' and doc_id is not '': #verfies if term is in the file
                    tfidf=float(text.count(term))/float(len(text)) * (float(log10(37497)/float(len(docIDs))))
                    index = {doc_id:tfidf} #creates the docID + tf
                    docIDs.append(index) #adds to list of docID's
                    df += 1
    sorted_data = sorted(docIDs, key=lambda item: tuple(item.values()), reverse = True)
    upload(term,sorted_data,df)

def read():
    terms = set() #adding values to a set to prevent additional copies 
    df = 0
    count = 0.0
    for root, dirs, files in os.walk("./WEBPAGES_RAW"):
        for name in files:
            if not name.endswith('.json') and not name.endswith('.tsv') and not name.endswith('.DS_Store'): 
                tf = 0
                index = {}
                document = os.path.join(root,name)
                file = open(document)
                text = parse(file)
                for i in text:
                    if i not in terms and i not in stop_words and i in words.words() or i in special_terms and len(i) > 1:
                        print(i)
                        terms.add(i)
                        createIndex(i)
                        
if __name__ == '__main__':
    read()

