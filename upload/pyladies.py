from connection import app_search, engine_name
from upload_to_appsearch import upload_dict
from convert_to_json import hash_id
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
            body={'query': 'Pyladies'},
            )
    ids = ([x['id']['raw'] for x in results['results']])
    app_search.delete_documents(
            engine_name=engine_name,
            body=ids
            )
            

def build_asset(location):
    url_stem = location.select('.chapter-name a')[0]['href']
    city = location.text.strip()

    if (name_root:= city.split(',')[0]).startswith('PyLadies'):
        name_root = name_root.split('PyLadies')[1].strip()

    name = 'PyLadies ' + name_root 
    logo = f"{pyl_root_url}{location.img['src'][2:]}"
    url = f"{pyl_root_url}{url_stem}"

    asset = {
            'id': hash_id(name+ url),
            'name': name,
            'organization_logo': logo,
            'city': city,
            'url': url, 
            'diversity_focus': ['Women in Tech'],
            'technology_focus': ['Python'],
            'parent_organization': 'PyLadies',
            'global_org_url_from_parent_organization': pyl_root_url,
            }

    links = location.select('h3.social-icons a'),

    for link in links[0]:
        if link['title'] != 'Contact':
            asset[link['title'].split(' ')[0].lower()] = link['href']
        
    return asset

if __name__ == '__main__':
    # delete_from_index()
    locations = [build_asset(location) for location in location_section]
    print(len(locations))
    # upload_dict(locations)
