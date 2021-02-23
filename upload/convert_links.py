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


    upload_dict(j)
