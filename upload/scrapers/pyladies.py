from connection import app_search, engine_name
from upload_to_appsearch import upload_dict
from convert_to_json import hash_id

import re
import httpx

from bs4 import BeautifulSoup

pyl_locations_page = httpx.get('https://pyladies.com/locations/')
soup = BeautifulSoup(pyl_locations_page.text, 'html.parser')
location_section = soup.select('#archive > article > div > div.chapter_location')
pyl_root_url = "https://pyladies.com"


def delete_from_index():
    """delete previous PyLadies Entries"""
    results = app_search.search(
            engine_name=engine_name,
            body={'query': 'PyLadies'},
            )
    ids = ([x['id']['raw'] for x in results['results']])
    app_search.delete_documents(
            engine_name=engine_name,
            body=ids
            )
            
def remove_from_city(city):
    """Strips 'PyLadies' from the location city"""
    if 'pyladies' in city.lower():
        return re.sub(r'PyLadies', '', city, re.I)
    return city

def generate_url(url_stem):
    """generate a url based on conditions"""

    if url_stem.startswith('/'):
        return f"{pyl_root_url}{url_stem}"

    if url_stem.startswith('http'):
        return url_stem

    return ''
        

def build_asset(location):
    url_stem = location.select('.chapter-name a')[0]['href']
    url = generate_url(url_stem)
    city = remove_from_city(location.text.strip())

    name_root = city.split(',')[0].strip()
    name = 'PyLadies ' + name_root 
    logo = f"{pyl_root_url}{location.img['src'][2:]}"

    asset = {
            'name': name,
            'organization_logo': logo,
            'city': city,
            'diversity_focus': ['Women in Tech'],
            'technology_focus': ['Python'],
            'parent_organization': 'PyLadies',
            'global_org_url_from_parent_organization': pyl_root_url,
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
    run()
