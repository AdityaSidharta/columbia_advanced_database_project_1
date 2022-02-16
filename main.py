import fire
import search
import display
import validity
import metrics
import model


def main(client_key, engine_key, precision, query):
    current_precision = 0.0
    initial_query = query
    while current_precision < precision:
        validity.assert_params(client_key, engine_key, query, precision)
        display.params(client_key, engine_key, query, precision)
        items = search.query(client_key, engine_key, query)
        relevant_items, nonrelevant_items = display.check_relevance(items)
        current_precision = metrics.calc_precision(relevant_items, nonrelevant_items)

        if current_precision == 0.0:
            display.failure(current_precision, precision, initial_query, query)
            break
        elif current_precision < precision:
            display.iterate(current_precision, precision, initial_query, query)
            proposed_query = model.improve(relevant_items, nonrelevant_items, query)
            new_query = model.order(relevant_items, nonrelevant_items, proposed_query)
            display.changes(query, new_query)
            query = new_query
        else:
            display.success(current_precision, precision, initial_query, query)
            break



if __name__ == '__main__':
    fire.Fire(main)
