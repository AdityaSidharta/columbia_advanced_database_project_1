#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().system('pip install google-api-python-client')
#Librarires download: numpy

# In[285]:

import numpy as np
def find_result(query):
    from googleapiclient.discovery import build
    import pprint
    rel=[]
    #define key
    api_key = "AIzaSyBx4fnqPbVC0BPRJxdIC0S3KR2PHNg2qPU"
    cse_key = "e8f624bdc54650190"

    resource = build("customsearch", 'v1', developerKey=api_key).cse()
    result = resource.list(q=query, cx=cse_key).execute()

    #pprint.pprint(result)

    for x in result['items']:
        print('\n')
        print("Title: ",x['title'])
        print("Link: ",x['link'])
        print("Description: ",x['snippet'])
        print('\n')
        val = input("Is this relevant? (y/n)")
        if(val == 'y'):
            res = {}
            res['title'] = x['title']
            res['link'] = x['link']
            res['description'] = x['snippet']
            rel.append(res)
    '''print("\nThe relevant ones are:")
    for x in rel:
        print('\n')
        print("Title: ",x['title'])
        print("Link: ",x['link'])
        print("Description: ",x['description'])
        print('\n\n')'''
    return rel

def precision(rel):
    precision = (len(rel)/10)
    return precision


# In[286]:


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
def preprocess(data):
    data = list(np.char.lower(data)) 
    stop_words = stopwords.words('english')
    new_data=[]
    for x in data:
        #print(x)
        if(x not in stop_words) and (x.isalnum() == True):
             new_data.append(x)
    return new_data
def stem(new_data):
    stemmer= PorterStemmer()
    new_data1=[]
    for x in new_data:
        new_data1.append(stemmer.stem(x))
    return new_data1


# In[287]:


def tokenization(rel):    
    from nltk.tokenize import word_tokenize
    data_title=[]
    data_body=[]
    data_original=[]
    for x in rel:
        data_title.append(stem(preprocess(word_tokenize(x['title']))))
        data_body.append(stem(preprocess(word_tokenize(x['description']))))
        data_original = data_original + preprocess(word_tokenize(x['description'])) +preprocess(word_tokenize(x['title']))
    original={}
    stemmer= PorterStemmer()
    for x in data_original:
        original[x] = stemmer.stem(x)
    return data_title, data_body, original


# In[288]:


def df(data_title, data_body):
    DF = {}
    for i in range(len(data_body)):
        tokens = data_body[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

    for i in range(len(data_title)):
        tokens = data_title[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

    for x in DF:
        DF[x] = len(DF[x])
    return DF


# In[289]:


def tfidf(rel, DF, data_title, data_body):
    from collections import Counter
    tf_idf = {}
    doc=0
    l=[]
    N = len(rel) #Number of relevant docs
    for i in range(len(rel)):
        tokens = data_body[i] + data_title[i]
        counter = Counter(tokens + data_title[i]) 
        #print(counter)#number of times each word occured in that doc
        words_count = len(tokens + data_title[i])   #total number of words in that doc
        for token in tokens:
            if(token not in tf_idf):
                tf = counter[token]/words_count  #tf of each word = number of times it occured / total number of words
                idf = np.log(N/DF[token])
                tf_idf[token] = tf*idf

    tf_idf_sort={}
    sorted_keys = sorted(tf_idf, key=tf_idf.get)
    for x in sorted_keys:
        tf_idf_sort[x] = tf_idf[x]
    return tf_idf_sort


# In[290]:


def get_key(val, original):
    for key, value in original.items():
         if val == value:
                return key
def get_query(q, tf_idf_sort, original):
    query=[]
    for x in tf_idf_sort:
        key = get_key(x, original)
        if(key not in q):
            query.append(x)
            if(len(query) ==2):
                break

    new_query = q +" "+ get_key(query[0], original) + " " +get_key(query[1], original)
    return new_query


# In[296]:


if __name__ == '__main__':
    import sys
    #print(len(sys.argv))
    q1=""
    #q = sys.argv[1]#input("Enter Query:")
    for x in range(1,len(sys.argv)-1):
        q1 = q1 + " "+ sys.argv[x]
    q = q1
    p = sys.argv[len(sys.argv)-1]
    p= float(p)#float(input("Enter Desired Precision (0 - 1.0):"))
    rel = find_result(q)
    preci = precision(rel)
    print("Precision: ", preci)
    for i in range(10):
        if(preci >= p) or (preci == 0):
            break
        else:
            data_title, data_body, original = tokenization(rel)
            DF = df(data_title, data_body)
            tf_idf = tfidf(rel, DF, data_title, data_body)
            new_query = get_query(q, tf_idf, original)
            q = new_query
            print("\nThe new suggested query is: ",new_query)
            rel = find_result(new_query)
            preci = precision(rel)
            print("\nThe Precision is: ", preci)

