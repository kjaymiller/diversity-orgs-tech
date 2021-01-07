import os
from elastic_enterprise_search import AppSearch

app_search = AppSearch(
        "https://cf0133fcec254cafba5f4ce69a3859a8.ent-search.eastus2.azure.elastic-cloud.com",
        http_auth=os.environ.get('PRIVATE_AUTH'),
        )

engine_name = os.environ.get('ENGINE_NAME')
