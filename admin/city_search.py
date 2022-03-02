from more_itertools import first_true
from connection import elastic_search
import googlemaps
import typing
import os
import logging

# REQUIRED: A VALID API KEY for the Google Maps API
GMAPS_KEY = os.environ.get("GMAPS_KEY", None)

if not GMAPS_KEY:
    raise ValueError("GMAPS_KEY not found. Please set the GMAPS_KEY environment variable")

gmaps = googlemaps.Client(key=os.environ.get("GMAPS_KEY", None))

def clean_spaces(replacement_char: str, /) -> str:
    """
    Removes double spaces in text.
    This cleans up information returned by google maps.
    
    param: replacement_char: character to replace the spaces with
    return: cleaned up text
    """
    return replacement_char.replace("  ", " ")


class City:
    """Google Maps Places Object Selected from a list of results. This makes interacting with the returned values easier"""
    def __init__(self, query: str):
        """
        Runs the query through places_autocomplete and selects the first result that is a city/town
        param: query: the query to be run
        """
        geocode_results = gmaps.places_autocomplete(
            input_text=query,
            types=["(cities)", "locality"]
        )
        
        if not geocode_results:
            raise ValueError(f"No results found for {query=}. Perhaps add a country code added to the query?")

        place_id = first_true(
            geocode_results,
            pred=lambda x:'locality' in x['types'],
        )['place_id']
        
        city = gmaps.place(
                place_id,
                fields=[
                    "type",
                    "geometry",
                    "name", "address_component",
                ]
        )
        
        for section in city['result']['address_components']:
            if 'locality' in section['types']:
                self.city = section['long_name']
        
            if 'administrative_area_level_1' in section['types']:
                self.region_long_name = section['long_name']
                self.region_short_name = section['short_name']
        
            if 'country' in section['types']:
                self.country_long_name = section['long_name']
                self.country_short_name = section['short_name']

        self.base_query = query
        self.place_id = place_id
        self.city = clean_spaces(city["result"]["name"])
        location = city["result"]["geometry"]["location"]
        self.location = f"{location['lat']}, {location['lng']}"
    
    @property    
    def city_name(self) -> str:
        """
        Return a string of the city name, region, and country. 
        If region is not present return the city and country to avoid confusion
        """

        if getattr(self, 'region_long_name', None):
            return clean_spaces(f"{self.city}, {self.region_long_name}{self.separator}{self.country_long_name}")
        
        else:
            return clean_spaces(f"{self.city}, {self.country_long_name}")


def city_search(document: dict[str, typing.Any], es_index: str) -> dict[str, typing.Any]:
    
    if city:=document['city'].lower() == 'online':
            logging.debug(f'skipping {city=} - location == Online') # Skip online-only locations (e.g. online-only events)
        
    else:
        query = document['city']
        es_query = {
                "match": {
                    "base_query": document['city']
                }
        }
    
        request = elastic_search.search(index=es_index, query=es_query)
        
        # If the document is not found, add it to the index
        if request['hits']['total']['value']:
            response = request['hits']['hits'][0]['_source']
            document.update(response)
                    
        else:
            city = City(query) # search google maps and build a city object
            city_doc = vars(city)
            elastic_search.index(
                index=es_index, document=city_doc, refresh=True
            )
            document.update(city_doc)
    return document