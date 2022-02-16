def params(client_key, engine_key, query, precision):
    print("Parameters:")
    print("Client key  = {}".format(client_key))
    print("Engine key  = {}".format(engine_key))
    print("Query       = {}".format(query))
    print("Precision   = {}".format(precision))

    print("Google Search Results:")
    print("======================")


def check_relevance(items):
    relevant_items = []
    nonrelevant_items = []
    assert len(items)
    for idx in range(len(items)):
        item = items[idx]
        title = item['title']
        url = item['url']
        summary = item['snippet']
        print("Result {}".format(idx))
        print("[")
        print("URL: {}".format(url))
        print("Title: {}".format(title))
        print("Summary: {}".format(summary))
        print("]")

        user_input = ''
        while user_input.lower() != 'y' and user_input.lower() != 'n':
            user_input = input("Relevant (Y/N)?")
            if user_input.lower == 'y':
                relevant_items.append(item)
            elif user_input.lower() == 'n':
                nonrelevant_items.append(item)
            else:
                print('Please try again. Only accepting input "y" or "n"')
    assert len(relevant_items) + len(nonrelevant_items) == len(items)
    return relevant_items, nonrelevant_items
