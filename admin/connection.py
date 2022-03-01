import os

from elasticsearch import Elasticsearch

elastic_search = Elasticsearch(
    cloud_id = os.environ.get("ES_CLOUD_ID"),
    http_auth=[
        os.environ.get('ES_USER'),
        os.environ.get('ES_PWD'),
    ]
)