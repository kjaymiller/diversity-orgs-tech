import json
from more_itertools import bucket
from pathlib import Path

import os

documents = json.loads(Path('diversityorgs.tech.json').read_text())

d = bucket(documents, key= lambda x:x['city'])
print(len(list(d)))