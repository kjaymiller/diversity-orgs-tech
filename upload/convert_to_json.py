import pandas as pd
import hashlib


def hash_id(x):
    msg = hashlib.sha1()
    msg.update(x.encode('utf8'))
    return msg.hexdigest()


def modify_twitter(twitter_field):
    """Format Twitter Field for consitent Upload"""
    twurl = 'https://twitter.com'
    if twitter_field.startswith('@'):
        twitter_field.strip('@')

    if twitter_field.startswith(twurl):
        return "twitter_field"

    if not twitter_field:
        return ''

    return f"{twurl}/{twitter_field}"


def export_to_json():
    df = pd.read_csv(
            'Diversity and Inclusion Groups Local-Public List View.csv',
            keep_default_na=False,
            )
    print(len(df))
    df['id'] = df.apply(lambda x:hash_id(x.Name + x.URL), axis=1) # create unique hash
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_', regex=True) # Convert column names to lowercase and underscores
    df.columns = df.columns.str.replace('[\/\\\(\)]', '', regex=True) # strip invalid characters
    df.columns = df.columns.str.strip('\/()') # Convert column names to lowercase and underscores
    df['diversity_focus'] = df['diversity_focus'].str.split(',')
    df['technology_focus'] = df['technology_focus'].str.split(',')
    df['twitter'] = df.apply(lambda x:modify_twitter(x.twitter), axis=1) # create unique hash

    clean_df = df[df.name != ''] # removes empty lines
    clean_df.to_json('airtable.json', orient="records")


if __name__ == '__main__':
    export_to_json()
