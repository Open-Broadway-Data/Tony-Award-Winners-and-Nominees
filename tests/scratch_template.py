"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils
import pandas as pd


# ------------------------------


# all_links = WikiScraper.get_links_for_tony_awards()
#
# # all_titles = []
# # Go through each page...
# for link in all_links[1:]:
#     wq = WikiScraper(link)
#     award_type = wq.wiki_title
#
#     break



# Continue here
# wq = WikiScraper('https://en.wikipedia.org/wiki/Tony_Award_for_Best_Direction_of_a_Musical')
# wq = WikiScraper('https://wikipedia.org/wiki/Tony_Award_for_Best_Performance_by_a_Leading_Actor_in_a_Musical')
award_type = wq.wiki_title
# print(award_type)

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



# Drop all those missing core cols -1
# core_cols = [x for x in records[0].keys() if not x.endswith('link')]
drop_rows = df[df[core_cols].isna().sum(axis=1)>0].index
print(f'Dropping {len(drop_rows):,} rows')
df.drop(drop_rows, inplace=True)
df.dropna(axis=1, how='all', inplace=True)

df


# df.isna().sum(axis=1).value_counts()

# If you want to save
if os.environ.get('SAVE',True):
    os.makedirs('data', exist_ok=True)
    name_root = wq.url.split('/')[-1]
    df_name = os.path.join('data', f'Wikipedia_scrape_{name_root}.csv')
    df.to_csv(df_name, index=False)









#
