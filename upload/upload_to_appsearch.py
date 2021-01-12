from connection import app_search, engine_name 
from more_itertools import chunked
import json


def upload():
    with open('airtable.json') as json_file:
        json_data = json.load(json_file)

    for body in chunked(json_data, 100):
        app_search.index_documents(
                engine_name=engine_name,
                body=body,
                )


if __name__ == '__main__':
    upload()
