from connection import app_search, engine_name
import json

if __name__ == '__main__':
    documents = []
    pages = app_search.list_documents(
            engine_name=engine_name,
            )['meta']['page']['total_pages']

    for page in range(1, pages + 1):
        documents.extend(app_search.list_documents(
            engine_name=engine_name,
            current_page=page,
            )['results']
        )

    with open('diversityorgs.tech.202102011619.json', 'w') as json_file:
        json.dump(documents, json_file)
