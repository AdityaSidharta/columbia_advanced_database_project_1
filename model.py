import numpy as np

import params
from process import process


def calc_precision(relevant_items, nonrelevant_items):
    return float(len(relevant_items) / (len(relevant_items) + len(nonrelevant_items)))


def rocchio(query_vector, relevant_vectors, nonrelevant_vectors):
    return (
        params.ALPHA * query_vector
        + params.BETA * (1.0 / len(relevant_vectors)) * np.sum(relevant_vectors, axis=0)
        - params.GAMMA * (1.0 / len(nonrelevant_vectors)) * np.sum(nonrelevant_vectors, axis=0)
    )


def get_query(new_query_vector, word2idx, idx2word, query_words, top_k=params.TOP_K):
    sorted_indices = list(new_query_vector.argsort()[::-1])
    query_indices = [word2idx[word] for word in query_words]
    proposed_indices = [x for x in sorted_indices if x not in query_indices][:top_k]
    proposed_words = [idx2word[idx] for idx in proposed_indices]
    proposed_score = [new_query_vector[idx] for idx in proposed_indices]
    sorted_words = [proposed_words for _, proposed_words in sorted(zip(proposed_score, proposed_words), reverse=True)]
    return ' '.join(query_words + sorted_words)


def get_query_dict(new_query_vector, word2idx):
    query_dict = {}
    for word, word_idx in word2idx.items():
        query_dict[word] = new_query_vector[word_idx]
    return query_dict


def improve(relevant_items, nonrelevant_items, query, prev_query_dict):
    unique_words = set()

    query_words, query_unique_words = query.lower().split(' '), set(query.lower().split(' '))
    relevant_tokens_words, relevant_unique_words = process(relevant_items, query_unique_words)
    nonrelevant_tokens_words, nonrelevant_unique_words = process(nonrelevant_items, query_unique_words)

    unique_words.update(query_unique_words)
    unique_words.update(relevant_unique_words)
    unique_words.update(nonrelevant_unique_words)

    word2idx, idx2word = get_word_index(unique_words)

    query_vector = get_query_vector(query_words, word2idx, prev_query_dict)
    relevant_vectors, nonrelevant_vectors = get_tfidf(relevant_tokens_words, nonrelevant_tokens_words, word2idx)
    new_query_vector = rocchio(query_vector, relevant_vectors, nonrelevant_vectors)

    new_query = get_query(new_query_vector, word2idx, idx2word, query_words)
    new_query_dict = get_query_dict(new_query_vector, word2idx)

    return new_query, new_query_dict


def get_tf(relevant_tokens_words, nonrelevant_tokens_words, word2idx):
    tf_dict = {}
    tokens = relevant_tokens_words + nonrelevant_tokens_words
    n_tokens = len(relevant_tokens_words) + len(nonrelevant_tokens_words)
    assert len(tokens) == n_tokens

    for _, word_idx in word2idx.items():
        tf_dict[word_idx] = {}
        for token_idx in range(n_tokens):
            tf_dict[word_idx][token_idx] = 0
    for token_idx, token in enumerate(tokens):
        n_words = 0.
        for word in token:
            word_idx = get_index(word, word2idx)
            if word_idx is not None:
                tf_dict[word_idx][token_idx] = tf_dict[word_idx][token_idx] + 1
                n_words = n_words + 1
        for _, word_idx in word2idx.items():
            tf_dict[word_idx][token_idx] = tf_dict[word_idx][token_idx] / n_words
    return tf_dict


def get_idf(relevant_tokens_words, nonrelevant_tokens_words, word2idx):
    idf_dict = {}
    tokens = relevant_tokens_words + nonrelevant_tokens_words
    n_tokens = len(relevant_tokens_words) + len(nonrelevant_tokens_words)
    assert len(tokens) == n_tokens

    for _, word_idx in word2idx.items():
        idf_dict[word_idx] = 0
    for token in tokens:
        for word in set(token):
            word_idx = get_index(word, word2idx)
            if word_idx is not None:
                idf_dict[word_idx] = idf_dict[word_idx] + 1
    for word_idx in idf_dict:
        idf_dict[word_idx] = np.log10(n_tokens / idf_dict[word_idx])
    return idf_dict


def get_tfidf(relevant_tokens_words, nonrelevant_tokens_words, word2idx):
    n_relevant = len(relevant_tokens_words)
    n_tokens = len(relevant_tokens_words) + len(nonrelevant_tokens_words)
    n_words = len(word2idx)
    result = np.zeros(shape=(n_tokens, n_words))

    tf_dict = get_tf(relevant_tokens_words, nonrelevant_tokens_words, word2idx)
    idf_dict = get_idf(relevant_tokens_words, nonrelevant_tokens_words, word2idx)

    for token_idx in range(n_tokens):
        for word_idx in range(n_words):
            result[token_idx][word_idx] = tf_dict[word_idx][token_idx] * idf_dict[word_idx]

    return result[:n_relevant, :], result[n_relevant:, :]


def get_query_vector(query_words, word2idx, prev_query_dict):
    n_words = len(word2idx)
    result = np.zeros(shape=(n_words,))
    if prev_query_dict is None:
        for word in query_words:
            word_idx = get_index(word, word2idx)
            if word_idx is not None:
                result[word_idx] = 1.
    else:
        for word, value in prev_query_dict.items():
            word_idx = get_index(word, word2idx)
            if word_idx is not None:
                result[word_idx] = value
    return result


def get_index(word, word2idx):
    if word not in word2idx:
        return None
    else:
        return word2idx[word]


def get_word_index(unique_words):
    word2idx = {}
    idx2word = {}
    list_unique_words = sorted(list(unique_words))
    for idx, word in enumerate(list_unique_words):
        word2idx[word] = idx
        idx2word[idx] = word
    return word2idx, idx2word
