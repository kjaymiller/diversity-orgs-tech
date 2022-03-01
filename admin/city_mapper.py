import json
import logging
import os
import typing
from operator import index
from pathlib import Path

import googlemaps
from elasticsearch.helpers import bulk
from more_itertools import bucket, first_true
import typer

from connection import elastic_search


def load_documents(json_file: str, bucket_key: str = 'city') -> typing.Sequence[list[dict[str, str]]]:
    """
    Buckets text into sequences segmented by the bucket key. 
    returns the objects bucketed by city"""
    return bucket(json.loads(Path(json_file).read_text()), key=lambda x:x[bucket_key])




def city_search(es_index: str, documents: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """
    Search for an existing value in Elasticsearch. 
    Add a reference document if one doesn't exist.
    Update the original document with the new location information.
    
    TODO: Should this be multiple functions?
    
    Currently updating documents is not supported and the entire index is rebuilt with this script.
    Use the flask app (app.py) for updating single documents. Bulk updates are not supported.
    """

    for document in documents:
        if 'id' in document:
            document.pop('id')


        yield document


def create_helper_index(es_index: str):
    """delete and recreate the index the cities that are in the update"""
    
    mappings = {
            "properties": {
                "location" : {
                    "type" : "geo_point"
                },
                "base_query": {
                    "type": "keyword"
                }
            }
    }
    
    elastic_search.indices.delete(index=es_index, ignore_unavailable=True)
    elastic_search.indices.create(index=es_index, mappings=mappings)


def reindex(es_index:str, mapping: dict[str, typing.Any]) -> None:
    """reindex the orgs that are in the update"""
    
    elastic_search.indices.delete(index=es_index, ignore_unavailable=True)
    elastic_search.indices.create(index=es_index, mappings=mapping)


def main(
    filenames: list[Path],
    es_index: str = typer.Option("", help="Elasticsearch Index for Technical Orgs", prompt=True),
    cities_index: str = typer.Option("", help="Elasticsearch Index for City References", prompt=True),
    ) -> None:

    for filename in ['a11y-list.json', 'diversityorgs.tech.json']:
        for group in buckets:
            bulk(
                client=elastic_search,
                index=es_index,
                actions=city_search(documents=buckets[group], es_index=cities_index),
                refresh=True,
                )


if __name__ == "__main__":
    typer.run(main) 