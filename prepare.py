import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------------

def basic_clean(article):
    '''
    This function takes in a article in string format.
    
    Turns all letters into lowercase.
    
    Normalizes the unicode characters using the NFKD method,
    while ignoring any unknow characters.
    
    Will replace anything that is NOT letters, numbers, whitespace or single quote.
    
    This funtion will return a basic cleaned article in string format
    '''
    
    # Lowercase 
    article = article.lower()
    
    # Normalization
    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    # Replace
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    
    return article

#-------------------------------------------------------------------------------------------------------------------------------

