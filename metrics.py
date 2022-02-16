# TODO: Improvement can include only caring about HTML files
def calc_precision(relevant_items, nonrelevant_items):
    return float(len(relevant_items) / (len(relevant_items) + len(nonrelevant_items)))
