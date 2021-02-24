import pandas as pd
import json
from upload_to_appsearch import upload_dict

with open("diversityorgs.tech.json") as json_file:
    j = (json.load(json_file))

    for i, val in enumerate(j):
        links = []

        for link in ['meetup', 'twitter', 'facebook']:
            if val.get(link):
                links.append(val[link])
                del val[link]
        if links:
            j[i]['links'] = links

    j = [x for x in j if x.get('parent_organization', '') != "Women Who Code"]

    upload_dict(j)

