import pandas as pd
import hashlib

def hash_id(x):
    msg = hashlib.sha1()
    msg.update(x.encode('utf8'))
    return msg.hexdigest()


df = pd.read_csv(
        'Diversity and Inclusion Groups Local-Public List View.csv',
        keep_default_na=False,
        )
df['id'] = df.apply(lambda x:hash_id(x.Name + x.URL), axis=1) # create unique hash
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_', regex=True) # Convert column names to lowercase and underscores
df.columns = df.columns.str.replace('[\/\\\(\)]', '', regex=True) # strip invalid characters
df.columns = df.columns.str.strip('\/()') # Convert column names to lowercase and underscores
df['diversity_focus'] = df.diversity_focus.str.split(',')
df['technology_focus'] = df.technology_focus.str.split(',')
clean_df = df[df.name != ''] # removes empty lines
clean_df.to_json('airtable.json', orient="records")
