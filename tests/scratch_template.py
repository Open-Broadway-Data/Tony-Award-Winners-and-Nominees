"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils
import pandas as pd
# ------------------------------

wq = WikiScraper(base_url)

# all_links= wq.get_links_for_tony_awards()


tables = wq.tables

# NEED TO DEBUG THE FOLLOWING CODE!
records = []

# Put them all together
for table in wq.tables:
    data = wq.get_data_from_table(table)
    records.extend(data)


df = pd.DataFrame(records)

df
