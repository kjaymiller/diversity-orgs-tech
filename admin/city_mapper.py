import googlemaps
import json
from more_itertools import bucket, first_true
from pathlib import Path
from connection import elastic_search, app_search
import os

gmaps = googlemaps.Client(key=os.environ.get("GMAPS_KEY"))
es_index = "cities_helper"

def clean_spaces(s):
    """removes double spaces in text"""
    return s.replace("  ", " ")

def load_documents(json_file: str):
    """Reads the json_file and returns the objects bucketed by city"""
    return bucket(json.loads(Path(json_file).read_text()), key=lambda x:x['city'])

class City:
    def __init__(self, query):
        self.base_query = query

        geocode_results = gmaps.places_autocomplete(
            input_text=query,
            types=["(cities)", "locality"]
        )
        
        place_id = first_true(
            geocode_results,
            pred=lambda x:'locality' in x['types']
        )['place_id']
        
        city = gmaps.place(
                place_id,
                fields=[
                    "type",
                    "geometry",
                    "name", "address_component",
                ]
        )
        
        if len(city["result"]["address_components"]) < 4: # Country and Not City
            self.region_short_name = ""
            self.region_long_name = ""
            self.country_long_name = clean_spaces(city['result']["address_components"][1]["long_name"])
            self.country_short_name = clean_spaces(city['result']["address_components"][1]["short_name"])
            separator= " "
            
        else:
            self.region_short_name = clean_spaces(city["result"]["address_components"][2]["short_name"])
            self.region_long_name = clean_spaces(city["result"]["address_components"][2]["long_name"])
            self.country_long_name = clean_spaces(city['result']["address_components"][3]["long_name"])
            self.country_short_name = clean_spaces(city['result']["address_components"][3]["short_name"])
            separator = ", "

        self.raw = city
        self.place_id = place_id
        self.city = clean_spaces(city["result"]["name"])
        location = city["result"]["geometry"]["location"]
        self.location = f"{location['lat']}, {location['lng']}"
        self.name = clean_spaces(f"{self.city}, {self.region_long_name}{separator}{self.country_long_name}")


def create_index():
    """index the cities that are in the update"""
    
    mappings = {
        "mappings": {
            "properties": {
                "location" : {
                    "type" : "geo_point"
                },
                "base_query": {
                    "type": "keyword"
                }
            }
        }
    }
    
    elastic_search.indices.delete(es_index)
    elastic_search.indices.create(es_index, body=mappings)


def city_search_gen(d: dict):
    docs = list(d)
    print(f"Searching for {docs[0]['city']}")
    
    for document in docs:
        document = city_search(document)
    
    return app_search.put_documents(
            engine_name=os.environ.get("ENGINE_NAME"),
            documents=docs,
    )


def city_search(document: dict):
    """process of searching for a value in Elasticsearch and 
add a places query if missing"""
    if document['city'].lower() == 'online':
        print('skipping Online')
    
    else:
        query = document['city']
        body = {
            "query": {
                "match": {
                    "base_query": document['city']
                }
            }
        }
    
        request = elastic_search.search(index=es_index, body=body)
        
        if request['hits']['total']['value']:
            response = request['hits']['hits'][0]['_source']
            document['city'] = response['name']
            document['location'] = response['location']
                      
        else:
            city = City(query) # search google maps and build a city object
            body = vars(city)
            elastic_search.index(
                index=es_index, body=body, refresh=True
            )
            document['city'] = city.name
    
    return document

def update_single_doc(document: dict):
    """Updates a single document using city_search"""
    
    document = city_search(document)
    
    return app_search.put_documents(
        engine_name=os.environ.get("ENGINE_NAME"),
        documents=[document],
    )


if __name__ == "__main__":
    # create_index()
    buckets = load_documents("diversityorgs.tech.json")
    # gv = buckets['Greenville, SC, USA']
    # for doc in gv:
    #    update_single_doc(doc)
        
    # for docs in buckets:
    #     city_search_gen(buckets[docs])