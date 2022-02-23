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
