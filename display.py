def params(client_key, engine_key, query, precision):
    print("Parameters:")
    print("Client key  = {}".format(client_key))
    print("Engine key  = {}".format(engine_key))
    print("Query       = {}".format(query))
    print("Precision   = {}".format(precision))

    print("Google Search Results:")
    print("======================")
    print("")


def check_relevance(items):
    relevant_items = []
    nonrelevant_items = []
    assert len(items)
    for idx in range(len(items)):
        item = items[idx]
        title = item["title"]
        url = item["link"]
        summary = item["snippet"]
        print("Result {}".format(idx + 1))
        print("[")
        print("URL: {}".format(url))
        print("Title: {}".format(title))
        print("Summary: {}".format(summary))
        print("]")

        user_input = ""
        while user_input.lower() != "y" and user_input.lower() != "n":
            user_input = input("Relevant (Y/N)?")
            if user_input.lower() == "y":
                relevant_items.append(item)
            elif user_input.lower() == "n":
                nonrelevant_items.append(item)
            else:
                print('Please try again. Only accepting input "y" or "n"')
        print("")
    assert len(relevant_items) + len(nonrelevant_items) == len(items)
    return relevant_items, nonrelevant_items


def failure(current_precision, precision, initial_query, query):
    print("None of the search results provided are relevant. The algorithm has been terminated [FAILURE].")
    print("Initial Query: {}".format(initial_query))
    print("Final Query : {}".format(query))
    print("Current Precision@10 : {}".format(current_precision))
    print("Target Precision@10 : {}".format(precision))
    print("")


def success(current_precision, precision, initial_query, query):
    print("The target precision has been achieved. The algorithm has been terminated [SUCCESS].")
    print("Initial Query : {}".format(initial_query))
    print("Final Query : {}".format(query))
    print("Current Precision@10 : {}".format(current_precision))
    print("Target Precision@10 : {}".format(precision))
    print("")


def changes(query, new_query):
    print("The query has been updated")
    print("Previous Query : {}".format(query))
    print("New Query : {}".format(new_query))
    print("")


def iterate(current_precision, precision, initial_query, query):
    print("Current precision is still below the target precision")
    print("Initial Query : {}".format(initial_query))
    print("Current Query : {}".format(query))
    print("Current Precision@10 : {}".format(current_precision))
    print("Target Precision@10 : {}".format(precision))
    print("Currently running the model to improve the query...")
    print("")
