import os

from elastic_enterprise_search import AppSearch

app_search = AppSearch(
    os.environ.get("CLOUD_URI"),
    http_auth=os.environ.get("PRIVATE_AUTH"),
)

engine_name = os.environ.get("ENGINE_NAME")