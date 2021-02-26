from connection import app_search, engine_name 
from convert_to_json import hash_id
from more_itertools import chunked
import json
import typer
import pathlib

def upload_dict(data):
    for body in chunked(data, 100):
        app_search.index_documents(
                engine_name=engine_name,
                documents=body,
                )


def upload(filename: typer.FileText, gen_ids: bool= typer.Option(False, '-i')):
    json_data = json.load(filename)

    if gen_ids:
        for entry in json_data:
            print(entry)
            entry['id'] = hash_id(entry['name'] + entry['url'])

    upload_dict(json_data)


if __name__ == '__main__':
    typer.run(upload)
