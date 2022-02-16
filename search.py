from googleapiclient.discovery import build


def query(client_key, engine_key, query):
    resource = build("customsearch", 'v1', developerKey=client_key).cse()
    result = resource.list(q=query, cx=engine_key).execute()
    return result['items']

