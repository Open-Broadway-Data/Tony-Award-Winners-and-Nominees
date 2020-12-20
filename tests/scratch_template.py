"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils
import pandas as pd
# ------------------------------


all_links = WikiScraper.get_links_for_tony_awards()

# Go through each page...
for link in all_links:
    None
    break

link





#
# tables = wq.tables
#
# # NEED TO DEBUG THE FOLLOWING CODE!
# records = []
#
# # Put them all together
# for table in wq.tables:
#     data = wq.get_data_from_table(table)
#     records.extend(data)
#
#
# df = pd.DataFrame(records)

# df
