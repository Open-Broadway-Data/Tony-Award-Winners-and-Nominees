"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')
import json

from scrape_wikipedia import WikiScraper, base_url, utils, methods
import pandas as pd


# ------------------------------


# This helpful function makes life a bit easier...
def get_dict_of_links_for_tony_awards():

    # Store the stuff here
    os.makedirs('data/internal', exist_ok=True)
    file_path = 'data/internal/all_tony_award_wikipedia_links.json'

    # If you have it, reload it...
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    all_links = WikiScraper.get_links_for_tony_awards()

    # Do this once...
    all_titles = {}
    # Go through each page...
    for link in all_links[1:]:

        if link in all_titles:
            continue

        wq = WikiScraper(link)
        award_type = wq.wiki_title

        all_titles[link] = award_type

    # Reverse the dict
    new_dict = {}
    for key, value in all_titles.items():

        # If the value already exists, it's a redirect. Choose the shorter url
        if value in new_dict:
            if len(key) < len(new_dict[value]):
                new_dict[value] = key
            continue
        # Otherwise, set the value and move on
        new_dict[value] = key

    # Save for future use
    with open(file_path, 'w') as f:
        json.dump(new_dict, f)

    # Now return
    return new_dict



# Get all links
all_links_dict = get_dict_of_links_for_tony_awards()


"""
Here's the ones we've tested:

X   Tony Award for Best Special Theatrical Event
    Tony Award for Best Revival of a Musical
X   Tony Award for Best Actor in a Play
X   Tony Award for Best Actor in a Musical
    Tony Award for Best Costume Design in a Musical
    Tony Award for Best Author
    Tony Award for Best Actress in a Musical
    Tony Award for Best Choreography
    Tony Award for Best Original Score
    Tony Award for Best Direction of a Play
    Tony Award for Best Costume Design in a Play
    Tony Award for Best Featured Actor in a Play
    Tony Award for Best Lighting Design
    Tony Award for Best Scenic Design in a Musical
    Tony Award for Best Conductor and Musical Director
    Tony Award for Best Featured Actress in a Musical
    Tony Award for Best Orchestrations
    Tony Award for Best Lighting Design in a Play
    Tony Award for Best Featured Actress in a Play
    Tony Award for Best Lighting Design in a Musical
    Tony Award for Best Revival of a Play
    Tony Award for Best Musical
    Tony Award for Best Actress in a Play
    Tony Award for Best Featured Actor in a Musical
X   Tony Award for Best Direction of a Musical
    Tony Award for Best Book of a Musical
    Tony Award for Best Scenic Design
    Tony Award for Best Costume Design
    Tony Award for Best Newcomer
    Tony Award for Best Play
    Tony Award for Best Stage Technician
    Tony Award for Best Sound Design
    Tony Award for Best Revival
    Tony Award for Best Scenic Design in a Play
"""


# Continue here -- Getting errors when parsing the individual table
next_key = 'Tony Award for Best Revival of a Musical'
wq = WikiScraper(all_links_dict[next_key])
award_type = wq.wiki_title

tables = wq.tables


records = []

# Put them all together
for table in wq.tables:
    data = wq.get_data_from_table(table)
    records.extend(data)



# ------------------------------------------------------------------------------
df = pd.DataFrame(records)
df.sort_values('year', inplace=True)




# get the 4 columns with the least na values
z = df.isna().sum().sort_values()
core_cols = z[z<z.median()].index.to_list()

if core_cols:

    # Drop all those missing core cols -1
    # core_cols = [x for x in records[0].keys() if not x.endswith('link')]
    drop_rows = df[df[core_cols].isna().sum(axis=1)>0].index
    print(f'Dropping {len(drop_rows):,} rows')
    df.drop(drop_rows, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)




# df.isna().sum(axis=1).value_counts()

# If you want to save
if os.environ.get('SAVE',True):
    os.makedirs('data', exist_ok=True)
    name_root = wq.url.split('/')[-1]
    df_name = os.path.join('data', f'Wikipedia_scrape_{name_root}.csv')
    df.to_csv(df_name, index=False)









#
