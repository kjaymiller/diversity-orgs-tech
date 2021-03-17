import httpx
from bs4 import BeautifulSoup
from cleanup import delete_from_index
from convert_to_json import hash_id
from upload_to_appsearch import upload_dict

bit_chapters_page = httpx.get("https://foundation.blacksintechnology.net/chapters/")
soup = BeautifulSoup(bit_chapters_page, "html.parser")
base_locations_wrapper = soup.select(".elementor-widget-wrap")


def get_locations():
    locations = []

    for location in base_locations_wrapper:

        if "Chapter Organizer" in location.text:
            name = location.select(".raven-heading-title")[0].text.strip()
            url = location.select("a.raven-button.raven-button-link")[0]["href"]
            asset = {
                "name": f"Blacks in Technology - {name}",
                "url": url,
                "organization_logo": "https://kjaymiller.s3-us-west-2.amazonaws.com/images/blacks-in-technology.jpeg",
                "city": name.title(),
                "diversity_focus": ["BIPOC"],
                "technology_focus": ["General Technology"],
                "parent_organization": "Blacks in Technology Foundation",
                "global_org_url_from_parent_organization": "https://blacksintechnology.net",
            }

            asset["id"] = hash_id(name + url)
            locations.append(asset)
    return locations


if __name__ == "__main__":
    delete_from_index("Blacks in Technology Foundation")
    upload_dict(get_locations())
