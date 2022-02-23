#!/usr/bin/env python
import numpy as np
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from process import preprocess, stem








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


if __name__ == '__main__':
    import sys
    q1=""
    for x in range(1,len(sys.argv)-1):
        q1 = q1 + " "+ sys.argv[x]
    q = q1
    p = sys.argv[len(sys.argv)-1]
    p = float(p)
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

