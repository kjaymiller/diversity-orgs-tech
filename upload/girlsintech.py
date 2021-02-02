from connection import app_search, engine_name
from upload_to_appsearch import upload_dict
from convert_to_json import hash_id

import re
import httpx

from bs4 import BeautifulSoup

with open('girlsintechNetworkList.html') as html_file:
    html = html_file.read()
    location_section = BeautifulSoup(html, 'html.parser').select('.card-wrap')


def delete_from_index():
    """delete previous Girls in Tech Entries"""
    results = app_search.search(
            engine_name=engine_name,
            body={'query': 'Girls in Tech'},
            )
    ids = ([x['id']['raw'] for x in results['results']])
    app_search.delete_documents(
            engine_name=engine_name,
            body=ids
            )
            

def build_asset(location):
    url = location.a['href']
    base_city = location.a.select('div.text p') or location.a.select('div.text h4')
    city = base_city[0].text
    name_root = location.a.select('div.text h4')[0].text
    name = 'Girls in Tech ' + name_root 
    logo = f"https://kjaymiller.s3-us-west-2.amazonaws.com/images/girlsintech.jpg"

    asset = {
            'name': name,
            'organization_logo': logo,
            'city': city,
            'url': url,
            'diversity_focus': ['Women in Tech'],
            'technology_focus': ['General Technology'],
            'parent_organization': 'Girls in Tech',
            'global_org_url_from_parent_organization': 'https://girlsintech.com',
            }

    asset['id'] = hash_id(name+ url)

    return asset


def test(value):
    locations = [build_asset(location) for location in location_section[1:]]
    print(locations)
    # print(sorted([location.get(value, '') for location in locations], reverse=True))


def run():
    delete_from_index()
    locations = [build_asset(location) for location in location_section[1:]]
    upload_dict(locations)


if __name__ == '__main__':
    # test('name') 
    run()
