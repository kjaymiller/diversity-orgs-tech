from connection import elastic_search
import os
import typer


es_index = os.environ.get("ES_INDEX")

def replace_term_in_field(field: str, term: str, replacement: str):
    """Replace a term in a field"""
    query = {
        "match": {
            field: term
            }
    }

    print(f"{query=}")
    results = elastic_search.search(index=es_index, query=query, size=1000)
    
    print(results)

    for doc in results['hits']['hits']:
        d = doc['_source']
        print(d['name'])
        if len(d[field]) == 1:
            d[field] = d[field][0].split(',') # Objects Listed as ['bipoc, women'] and not ['bipoc', 'women']
        
        d[field] = [replacement if i == term else i.strip() for i in d[field]]
        elastic_search.index(index=es_index, id=doc['_id'], document=d)   


def youth_in_diversity_field():
    query = {
        "match": {
            "technology_focus": "youth education"
        }
    }

    results = elastic_search.search(index=es_index, query=query, size=1000)
    
    for doc in results['hits']['hits']:
        d = doc['_source']

        if len(d['technology_focus']) == 1:
            d['technology_focus'] = d['technology_focus'][0].split(',') # Objects Listed as ['bipoc, women'] and not ['bipoc', 'women']

        if 'Youth Education' in d['technology_focus']:
            print(d['name'], d['technology_focus'])
            d['technology_focus'].remove('Youth Education')
            
        if 'youth' not in d['diversity_focus']:
            d['diversity_focus'].append('Youth Education')
        
        elastic_search.index(index=es_index, id=doc['_id'], document=d)   



def remove_duplicates(field: str):
    """Remove duplicates from a field"""
    query = {
        "match_all": {}
    }

    results = elastic_search.search(index=es_index, query=query, size=1000)
    
    for doc in results['hits']['hits']:
        d = doc['_source']
        d[field] = list(set(d[field]))
        elastic_search.index(index=es_index, id=doc['_id'], document=d)
    

if __name__ == "__main__":
    # replace_term_in_field('diversity_focus', 'Youth Education', 'youth')
    remove_duplicates('diversity_focus')