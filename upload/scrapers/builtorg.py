from connection import app_search, engine_name
from upload_to_appsearch import upload_dict
from convert_to_json import hash_id
from cleanup import delete_from_index

import re
import httpx

from bs4 import BeautifulSoup

with open('upload/builtorg.html') as html_file:
    soup = BeautifulSoup(html_file.read(), 'html.parser')
    location_section = soup.select('a')
            
def get_locations():
    locations = []

    for location in location_section:
        url = location['href']
        base_name = location.text.strip()
        city = base_name
        name = 'BUILT ' + city

        asset = {
            'name': name,
            'organization_logo': 'https://builtinternational.org/wp-content/uploads/2020/11/INTERNATIONAL-1X.png',
            'meetup': url,
            'url': url,
            'city': city,
            'diversity_focus': ['BIPOC'],
            'technology_focus': ['General Technology'],
            'parent_organization': 'Blacks United in Leading Technology International',
            'global_org_url_from_parent_organization': 'https://builtinternational.org',
            }

        asset['id'] = hash_id(name+ url)
        locations.append(asset)
    return locations


def run():
    delete_from_index('BUILT')
    upload_dict(get_locations())


if __name__ == '__main__':
    run()

