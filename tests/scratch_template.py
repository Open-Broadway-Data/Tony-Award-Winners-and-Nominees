"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils
import pandas as pd


# ------------------------------


all_links = WikiScraper.get_links_for_tony_awards()

# all_titles = []
# Go through each page...
for link in all_links[1:]:
    wq = WikiScraper(link)
    award_type = wq.wiki_title

    break
    
# Continue here


wq = WikiScraper('https://en.wikipedia.org/wiki/Tony_Award_for_Best_Direction_of_a_Musical')
award_type = wq.wiki_title
print(award_type)

tables = wq.tables


records = []

# Put them all together
for table in wq.tables:
    data = wq.get_data_from_table(table)
    records.extend(data)
# table



df = pd.DataFrame(records)
df.sort_values('year', inplace=True)



# If you want to save
if os.environ.get('SAVE',True):
    os.makedirs('data', exist_ok=True)
    name_root = wq.url.split('/')[-1]
    df_name = os.path.join('data', f'Wikipedia_scrape_{name_root}.csv')
    df.to_csv(df_name, index=False)









#
