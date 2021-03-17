import re

import httpx
from bs4 import BeautifulSoup
from convert_to_json import hash_id

from cleanup import delete_from_index
from connection import app_search, engine_name
from upload_to_appsearch import upload_dict

wwgo_location_page = httpx.get("http://www.womenwhogo.org")
soup = BeautifulSoup(wwgo_location_page, "html.parser")
region_wrapper = soup.select("div.row.chapter-region")


def get_locations():
    locations = []

    for region_group in region_wrapper:
        region = region_group.select("div.col-xs-12 p")[0].text.strip()
        region = re.sub(r"\.", "", region)
        location = region_group.find_next_sibling("div")

        while "chapter-region" not in location.get("class", ""):
            base_name = location.select("p")[0].text.strip().rstrip(":")
            city = f"{base_name}, {region}"
            links = location.select("a")
            asset = {
                "name": f"Women Who Go - {base_name}",
                "organization_logo": "http://www.womenwhogo.org/assets/images/wwglogo.png",
                "city": city.strip(),
                "diversity_focus": ["Women"],
                "technology_focus": ["Go"],
                "parent_organization": "Women Who Go",
                "global_org_url_from_parent_organization": "https://womenwhogo.org",
            }

            for link in links:
                url = link["href"]

                if "meetup.com" in url:
                    asset["meetup"] = url
                    asset["url"] = url
                    continue

                if "conpass.com" in url:
                    asset["meetup"] = url
                    asset["url"] = url
                    continue

                if "facebook.com" in url:
                    asset["facebook"] = url
                    continue

                if "twitter.com" in url:
                    asset["twitter"] = url
                    continue

            asset["id"] = hash_id(base_name + url)
            locations.append(asset)
            location = location.find_next_sibling("div")

            if not location:  # ran into issues where this would short-circuit
                location = {"class": "chapter-region"}

    return locations


def run():
    delete_from_index("Women Who Go")
    upload_dict(get_locations())


if __name__ == "__main__":
    run()
    # print(get_locations())
