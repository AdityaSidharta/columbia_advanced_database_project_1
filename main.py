import fire

import display
import model
import search
import validity


def main(client_key, engine_key, precision, query):
    current_precision = 0.0
    initial_query = query
    query_dict = None
    while current_precision < precision:
        validity.assert_params(client_key, engine_key, query, precision)
        display.params(client_key, engine_key, query, precision)
        items = search.query(client_key, engine_key, query)
        relevant_items, nonrelevant_items = display.check_relevance(items)
        current_precision = model.calc_precision(relevant_items, nonrelevant_items)

        if current_precision == 0.0:
            display.failure(current_precision, precision, initial_query, query)
            break
        elif current_precision < precision:
            display.iterate(current_precision, precision, initial_query, query)
            proposed_query, proposed_query_dict = model.improve(relevant_items, nonrelevant_items, query, query_dict)
            display.changes(query, proposed_query)
            query = proposed_query
            query_dict = proposed_query_dict
        else:
            display.success(current_precision, precision, initial_query, query)
            break


if __name__ == "__main__":
    fire.Fire(main)
