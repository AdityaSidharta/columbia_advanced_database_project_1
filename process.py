import numpy as np
from nltk.corpus import stopwords

from params import STEMMER, TOKENIZER
from nltk.stem.arlstem2 import ARLSTem2
from nltk.stem.arlstem import ARLSTem
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
from variables import LANGUAGE


def get_stemmer():
    if STEMMER == 'none':
        return None
    elif STEMMER == 'porter':
        return PorterStemmer()
    elif STEMMER == 'snowball':
        return SnowballStemmer(LANGUAGE)
    elif STEMMER == 'arlstem':
        return ARLSTem()
    elif STEMMER == 'arlstem2':
        return ARLSTem2()
    else:
        raise ValueError("STEMMER must be one of ['none', 'porter', 'snowball', 'arlstem', 'arlstem2']. Current Value "
                         ": {}".format(STEMMER))


def get_tokenizer():
    if TOKENIZER == 'word':
        return word_tokenize
    elif TOKENIZER == 'wordpunct':
        return wordpunct_tokenize
    elif TOKENIZER == 'stanford':
        return StanfordTokenizer().tokenize
    elif TOKENIZER == 'treebank':
        return TreebankWordTokenizer().tokenize
    else:
        raise ValueError("TOKENIZER must be one of ['word', 'wordpunct', 'stanford', 'treebank']. Current Value : {}".format(TOKENIZER))


def preprocess(document):
    words = list(np.char.lower(document).split(' '))
    stop_words = stopwords.words(LANGUAGE)
    result_words = []
    for word in words:
        if(word not in stop_words) and (word.isalnum()):
            result_words.append(word)
    return result_words


def stem(words):
    stemmer = get_stemmer()
    if stemmer is None:
        return words
    else:
        result_words = []
        for word in words:
            result_words.append(stemmer.stem(word))
    return result_words


def tokenize(document):
    tokenizer = get_tokenizer()
    return tokenizer(document)


def flatten(t):
    return [item for sublist in t for item in sublist]


def process(items):
    tokens_words = []
    unique_words = set()
    for item in items:
        document_title = item['title']
        document_body = item['description']
        words_title = stem(preprocess(tokenize(document_title)))
        words_body = stem(preprocess(tokenize(document_body)))
        tokens_words.append(words_title + words_body)
        unique_words.update(words_title)
        unique_words.update(words_body)
    return tokens_words, unique_words


def get_word_index(unique_words):
    word2idx = {}
    idx2word = {}
    list_unique_words = list(unique_words)
    for idx, word in enumerate(list_unique_words):
        word2idx[word] = idx
        idx2word[idx] = word
    return word2idx, idx2word


def get_index(word, word2idx):
    if word not in word2idx:
        return None
    else:
        return word2idx[word]


def idf(relevant_tokens_words, nonrelevant_tokens_words, word2idx):
    idf_dict = {}
    n_documents = len(relevant_tokens_words,)
    for word, idx in word2idx.items():
        idf_dict[idx] = 0
    for tokens in [relevant_tokens_words, nonrelevant_tokens_words]:
        for token in tokens:
            for word in set(token):
                idx = get_index(word, word2idx)
                if idx is not None:
                    idf_dict[idx] = idf_dict[idx] + 1
    for idx in idf_dict:
        idf_dict[idx] = np.log10(len(relevant_tokens_words) + len(nonrelevant_tokens_words))
    return idf_dict


def tf(relevant_tokens_words, nonrelevant_token_words, word2idx):
    tf_dict = {}


def tfidf(rel, DF, data_title, data_body):
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