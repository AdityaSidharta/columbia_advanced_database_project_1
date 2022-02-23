import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.arlstem import ARLSTem
from nltk.stem.arlstem2 import ARLSTem2
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize.stanford import StanfordTokenizer

from params import STEMMER, TOKENIZER, LANGUAGE

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


def get_stemmer():
    if STEMMER == "none":
        return None
    elif STEMMER == "porter":
        return PorterStemmer().stem
    elif STEMMER == "snowball":
        return SnowballStemmer(LANGUAGE).stem
    elif STEMMER == "arlstem":
        return ARLSTem().stem
    elif STEMMER == "arlstem2":
        return ARLSTem2().stem
    elif STEMMER == "lemmatize":
        return WordNetLemmatizer().lemmatize
    else:
        raise ValueError(
            "STEMMER must be one of ['none', 'porter', 'snowball', 'arlstem', 'arlstem2', 'lemmatize']. Current Value "
            ": {}".format(STEMMER)
        )


def get_tokenizer():
    if TOKENIZER == "word":
        return word_tokenize
    elif TOKENIZER == "wordpunct":
        return wordpunct_tokenize
    elif TOKENIZER == "stanford":
        return StanfordTokenizer().tokenize
    elif TOKENIZER == "treebank":
        return TreebankWordTokenizer().tokenize
    else:
        raise ValueError(
            "TOKENIZER must be one of ['word', 'wordpunct', 'stanford', 'treebank']. Current Value : {}".format(
                TOKENIZER
            )
        )


def preprocess(words, query_unique_words):
    stop_words = stopwords.words(LANGUAGE)
    result_words = []
    for word in words:
        if word in query_unique_words:
            result_words.append(word)
        elif (word not in stop_words) and (word.isalnum()):
            result_words.append(word)
    return result_words


def stem(words, query_unique_words):
    stemmer = get_stemmer()
    if stemmer is None:
        return words
    else:
        result_words = []
        for word in words:
            if word in query_unique_words:
                result_words.append(word)
            else:
                result_words.append(stemmer(word))
    return result_words


def tokenize(document):
    tokenizer = get_tokenizer()
    return [x.lower() for x in tokenizer(document)]


def flatten(t):
    return [item for sublist in t for item in sublist]


def process(items, query_unique_words):
    tokens_words = []
    unique_words = set()
    for item in items:
        document_title = item["title"]
        document_body = item["snippet"]
        words_title = stem(preprocess(tokenize(document_title), query_unique_words), query_unique_words)
        words_body = stem(preprocess(tokenize(document_body), query_unique_words), query_unique_words)
        tokens_words.append(words_title + words_body)
        unique_words.update(words_title)
        unique_words.update(words_body)
    return tokens_words, unique_words
