"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils, methods
import pandas as pd


# ------------------------------

# Get all links
all_links_dict = methods.get_dict_of_links_for_tony_awards()

"""
Here's the ones we've tested:
	Tony Award for Best Actor in a Musical
	Tony Award for Best Actor in a Play
	Tony Award for Best Actress in a Musical
	Tony Award for Best Actress in a Play
	Tony Award for Best Author
	Tony Award for Best Book of a Musical
	Tony Award for Best Choreography
	Tony Award for Best Conductor and Musical Director
	Tony Award for Best Costume Design
	Tony Award for Best Costume Design in a Musical
	Tony Award for Best Costume Design in a Play
	Tony Award for Best Direction of a Musical
	Tony Award for Best Direction of a Play
	Tony Award for Best Director
	Tony Award for Best Featured Actor in a Musical
	Tony Award for Best Featured Actor in a Play
	Tony Award for Best Featured Actress in a Musical
	Tony Award for Best Featured Actress in a Play
	Tony Award for Best Lighting Design
	Tony Award for Best Lighting Design in a Musical
	Tony Award for Best Lighting Design in a Play
	Tony Award for Best Musical
	Tony Award for Best Newcomer
	Tony Award for Best Orchestrations
	Tony Award for Best Original Score
	Tony Award for Best Play
	Tony Award for Best Revival
	Tony Award for Best Revival of a Musical
	Tony Award for Best Revival of a Play
	Tony Award for Best Scenic Design
	Tony Award for Best Scenic Design in a Musical
	Tony Award for Best Scenic Design in a Play
	Tony Award for Best Sound Design
X	Tony Award for Best Special Theatrical Event
	Tony Award for Best Stage Technician
"""


# Continue here -- Getting errors when parsing the individual table
next_key = 'Tony Award for Best Actor in a Musical'
wq = WikiScraper(all_links_dict[next_key])
award_type = wq.wiki_title



records = []

# Put them all together
for table in wq.tables:
    data = wq.get_data_from_table(table)
    records.extend(data)

# ------------------------------------------------------------------------------
df = pd.DataFrame(records)
n_orig = len(df)

# Now drop
df = df[~df['year'].isna()]
n_new = len(df)

print(f'dropping {n_orig-n_new:,} rows')
df.sort_values('year', inplace=True)


# WE DON'T NEED THIS COMPLICATED BUSINESS BELOW...
# # get the 4 columns with the least na values
# z = df.isna().sum().sort_values()
# core_cols = z[z<z.median()].index.to_list()
#
# if core_cols:
#
#     # Drop all those missing core cols -1
#     # core_cols = [x for x in records[0].keys() if not x.endswith('link')]
#     drop_rows = df[df[core_cols].isna().sum(axis=1)>0].index
#     print(f'Dropping {len(drop_rows):,} rows')
#     df.drop(drop_rows, inplace=True)
#     df.dropna(axis=1, how='all', inplace=True)


# df.isna().sum(axis=1).value_counts()

# If you want to save
if os.environ.get('SAVE',True):
    os.makedirs('data', exist_ok=True)
    name_root = wq.url.split('/')[-1]
    df_name = os.path.join('data', f'Wikipedia_scrape_{name_root}.csv')
    df.to_csv(df_name, index=False)









#
