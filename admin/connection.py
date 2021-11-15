import os

from elastic_enterprise_search import AppSearch
from elasticsearch import Elasticsearch

app_search = AppSearch(
    os.environ.get("ES_ENT_CLOUD_URI"),
    http_auth=os.environ.get("PRIVATE_AUTH"),
)

engine_name = os.environ.get("ENGINE_NAME")

elastic_search = Elasticsearch(
    cloud_id = os.environ.get("ES_CLOUD_ID"),
    http_auth=[
        os.environ.get('ES_USER'),
        os.environ.get('ES_PWD'),
    ]
)