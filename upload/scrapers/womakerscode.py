import re

import httpx
from bs4 import BeautifulSoup
from convert_to_json import hash_id

from cleanup import delete_from_index
from connection import app_search, engine_name
from upload_to_appsearch import upload_dict

womakers_location_page = httpx.get("https://womakerscode.org/locations")
soup = BeautifulSoup(womakers_location_page, "html.parser")
base_locations_wrapper = soup.select("div.container-cities")


def get_locations():
    locations = []

    for location in base_locations_wrapper:

        name = location.select("h3")[0].text.strip()
        url = location.select("a")[0]["href"]
        city, region = location.select("strong")[0].text.strip().split("/")

        city = str(city or name).strip()

        asset = {
            "name": f"WoMakersCode - {name}",
            "url": url,
            "organization_logo": "https://d33wubrfki0l68.cloudfront.net/16a1903b64a4d7e982440dec57fe954c2273d95b/90edb/assets/images/womakerscode-icone.png",
            "city": f"{city}, {region}".strip(),
            "diversity_focus": ["Women in Tech"],
            "technology_focus": ["General Technology"],
            "parent_organization": "WoMakersCode",
            "global_org_url_from_parent_organization": "https://womakerscode.org",
        }

        asset["id"] = hash_id(name + url)
        locations.append(asset)
    return locations


def run():
    delete_from_index("WoMakersCode")
    upload_dict(get_locations())


if __name__ == "__main__":
    # test()
    run()
    # print(soup.prettify())
