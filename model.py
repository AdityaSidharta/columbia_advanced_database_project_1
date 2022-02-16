import numpy as np

import params


def rocchio(query_vector, relevant_vectors, nonrelevant_vectors):
    return (
        params.ALPHA * query_vector
        + params.BETA * (1.0 / len(relevant_vectors)) * np.sum(relevant_vectors)
        - params.GAMMA * (1.0 / len(nonrelevant_vectors)) * np.sum(nonrelevant_vectors)
    )


def improve(relevant_items, non_relevant_items, query):
    # TODO: implement improve()
    return query


def order(relevant_items, non_relevant_items, proposed_query):
    # TODO: implement order()
    return proposed_query
