"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils, methods
import numpy as np
import pandas as pd

pd.options.display.max_rows = 100

# ------------------------------

# Get all links
all_links_dict = methods.get_dict_of_links_for_tony_awards()

"""
Here's the ones we've tested:
- [X]	Tony Award for Best Actor in a Musical
- [X]	Tony Award for Best Actor in a Play
- [X]	Tony Award for Best Actress in a Musical
- [X]	Tony Award for Best Actress in a Play
- [X]	Tony Award for Best Author
- [X]	Tony Award for Best Book of a Musical
- [X]	Tony Award for Best Choreography
- [X]	Tony Award for Best Conductor and Musical Director
- [X]	Tony Award for Best Costume Design
- [X]	Tony Award for Best Costume Design in a Musical
- [X]	Tony Award for Best Costume Design in a Play
- [X]	Tony Award for Best Direction of a Musical
- [X]	Tony Award for Best Direction of a Play
- [X]	Tony Award for Best Director
- [X]	Tony Award for Best Featured Actor in a Musical
- [X]	Tony Award for Best Featured Actor in a Play
- [X]	Tony Award for Best Featured Actress in a Musical
- [X]	Tony Award for Best Featured Actress in a Play
- [X]	Tony Award for Best Lighting Design <-------- Begining to revise directly on wikipedia page.
- [X]	Tony Award for Best Lighting Design in a Musical
- [X]	Tony Award for Best Lighting Design in a Play
- [X]	Tony Award for Best Musical
- [X]	Tony Award for Best Newcomer
- [X]	Tony Award for Best Orchestrations
- [X]	Tony Award for Best Original Score
- [X]	Tony Award for Best Play
- [X]	Tony Award for Best Revival
- [X]	Tony Award for Best Revival of a Musical
- [X]	Tony Award for Best Revival of a Play
- [X]	Tony Award for Best Scenic Design
- [X]	Tony Award for Best Scenic Design in a Musical
- [X]	Tony Award for Best Scenic Design in a Play
- [X]	Tony Award for Best Sound Design
- [X]	Tony Award for Best Special Theatrical Event
- [X]	Tony Award for Best Stage Technician
"""


# Continue here -- Getting errors when parsing the individual table
next_key = 'Tony Award for Best Featured Actress in a Play'

for next_key in list(all_links_dict.keys()):


	wq = WikiScraper(all_links_dict[next_key])
	award_type = wq.wiki_title

	records = wq.get_data_from_all_tables()
	records = wq.clean_tony_award_wiki_data(records, wiki_title=wq.wiki_title)
	wq.validate_tony_award_wiki_data(records, wiki_title=wq.wiki_title)

	# -----------------------------------------------------------------------------

	df = pd.DataFrame(records)

	# If you want to save
	if os.environ.get('SAVE',True):
	    os.makedirs('data', exist_ok=True)
	    name_root = wq.url.split('/')[-1]
	    df_name = os.path.join('data', f'Wikipedia_scrape_{name_root}.csv')
	    df.to_csv(df_name, index=False)



#
