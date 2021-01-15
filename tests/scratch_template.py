"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils, methods
import numpy as np
import pandas as pd

pd.options.display.max_rows = 100

wq = WikiScraper(url=None)
data = wq.get_all_tony_award_data(save=True)



# Now you can reference individual items in the data and build a dataframe for it.
# Very useful for testing data quality.
for key, value in data.items():
	print(key)
	continue
	df = pd.DataFrame(value)
	if 'award_name' not in df.columns:
		df['award_name'] = key
	break

df.head(5)

# foo
