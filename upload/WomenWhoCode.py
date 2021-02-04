from connection import app_search, engine_name
from upload_to_appsearch import upload_dict
from convert_to_json import hash_id

import re
import httpx

from bs4 import BeautifulSoup
url_root = 'https://womenwhocode.org'

with open('upload/WomenWhoCodeNetworkList.html') as html_file:
    soup = BeautifulSoup(html_file.read(), 'html.parser')
    location_section = soup.select('.network-box-wrapper')


def delete_from_index():
    """delete previous Women Who Code Entries"""
    results = app_search.search(
            engine_name=engine_name,
            body={'query': 'Women Who Code'},
            )
    ids = ([x['id']['raw'] for x in results['results']])
    app_search.delete_documents(
            engine_name=engine_name,
            body=ids
            )
            
def build_asset(location):
    href = location.select('.network-img-container a')[0]['href']
    url = f"{url_root}/{href}"
    base_city = location.select('h3.network-name')[0].text.lstrip('WWCode')
    region = location.select('p.network-country')[0].text

    city = f"{base_city}, {region}"
    name = 'Women Who Code ' + base_city
    asset = {
            'name': name,
            'organization_logo': 'https://kjaymiller.s3-us-west-2.amazonaws.com/images/WWCode_logo_official.png',
            'city': city,
            'diversity_focus': ['Women in Tech'],
            'technology_focus': ['General Technology'],
            'parent_organization': 'Women Who Code',
            'global_org_url_from_parent_organization': 'https://womenwhocode.org',
            }

    asset['id'] = hash_id(name+ url)

    if url:
        asset['url'] = url

    links = location.select('h3.social-icons a'),

    for link in links[0]:
        if link['title'] not in ['Contact', 'website']:
            asset[link['title'].split(' ')[0].lower()] = link['href']
        
    return asset


def test(value = ''):
    locations = [build_asset(location) for location in location_section]

    if value:
        print(sorted([location.get(value, '') for location in locations], reverse=True))

    else:
        print(locations)


def run():
    delete_from_index()
    locations = [build_asset(location) for location in location_section]
    upload_dict(locations)


if __name__ == '__main__':
    # test() 
    run()
    # print(soup.prettify())
