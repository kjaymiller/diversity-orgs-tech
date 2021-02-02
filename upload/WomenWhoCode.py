from connection import app_search, engine_name
from upload_to_appsearch import upload_dict
from convert_to_json import hash_id

import re
import httpx

from bs4 import BeautifulSoup

with open('upload/WomenWhoCodeNetworkList.html') as html_file:
    soup = BeautifulSoup(html_file.read(), 'html.parser')
    location_section = soup.select('div > div')


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
            

def remove_from_city(city):
    """Strips 'Women Who Code' from the location city"""
    if 'Women Who Code' in city.lower():
        return re.sub(r'WWCode', '', city, re.I)
    return city


def generate_url(url_stem):
    """generate a url based on conditions"""
    return f"{wwc_root_url}{url_stem}"

        
def build_asset(location):
    url_stem = location.select('.network-img-container a')[0]['href']
    url = generate_url(url_stem)
    city = remove_from_city(location.text.strip())

    name_root = city.split(',')[0].strip()
    name = 'Women Who Code ' + name_root 
    logo = f"{wwc_root_url}{location.img['src'][2:]}"

    asset = {
            'name': name,
            'organization_logo': logo,
            'city': city,
            'diversity_focus': ['Women in Tech'],
            'technology_focus': ['General Technolofy'],
            'parent_organization': 'Women Who Code',
            'global_org_url_from_parent_organization': wwc_root_url,
            }

    asset['id'] = hash_id(name+ url)

    if url:
        asset['url'] = url

    links = location.select('h3.social-icons a'),

    for link in links[0]:
        if link['title'] not in ['Contact', 'website']:
            asset[link['title'].split(' ')[0].lower()] = link['href']
        
    return asset


def test(value):
    locations = [build_asset(location) for location in location_section]
    print(sorted([location.get(value, '') for location in locations], reverse=True))


def run():
    delete_from_index()
    locations = [build_asset(location) for location in location_section]
    upload_dict(locations)


if __name__ == '__main__':
    # test('name') 
    # run()
    print(soup.prettify())
