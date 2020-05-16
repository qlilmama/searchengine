from bs4 import BeautifulSoup
from collections import defaultdict
import pymongo
import json
import os
import re
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def parse(file):
    soup = BeautifulSoup(file,'lxml')
    text = soup.get_text()
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    text = text.lower()
    text = word_tokenize(text)
    return text
    

    
