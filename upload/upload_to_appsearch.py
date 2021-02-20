from connection import app_search, engine_name 
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


def upload(filename: typer.FileText):
    json_data = json.load(filename)
    upload_dict(json_data)


if __name__ == '__main__':
    typer.run(upload)
