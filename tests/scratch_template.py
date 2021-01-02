"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url, utils, methods
import numpy as np
import pandas as pd

pd.options.display.max_rows = 50

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
- [ ]	Tony Award for Best Featured Actress in a Play  <-------- Consider revising directly on Wikipedia...
- [X]	Tony Award for Best Lighting Design <-------- Has data for best play and best musical on the same page...
- [X]	Tony Award for Best Lighting Design in a Musical
- [X]	Tony Award for Best Lighting Design in a Play
- [X]	Tony Award for Best Musical
- [X]	Tony Award for Best Newcomer
- [X]	Tony Award for Best Orchestrations
- [X]	Tony Award for Best Original Score
- [X]	Tony Award for Best Play
- [X]	Tony Award for Best Revival
- [X]	Tony Award for Best Revival of a Musical <------ Need to reconcile values which span multiple rows... (Create a map of indixes to values... This can potentially be used to solve index col issues)
- [X]	Tony Award for Best Revival of a Play
- [X]	Tony Award for Best Scenic Design
- [X]	Tony Award for Best Scenic Design in a Musical
- [X]	Tony Award for Best Scenic Design in a Play
- [ ]	Tony Award for Best Sound Design <------ No tables on this page... Need to go and create them
- [ ]	Tony Award for Best Special Theatrical Event
- [ ]	Tony Award for Best Stage Technician <------ Need to reconcile values which span multiple rows
"""


# Continue here -- Getting errors when parsing the individual table
next_key = 'Tony Award for Best Lighting Design in a Musical'

len(all_links_dict)

for next_key in list(all_links_dict.keys()):


	wq = WikiScraper(all_links_dict[next_key])
	award_type = wq.wiki_title
	print(award_type)
	print(wq.url)

	if award_type=='Tony Award for Best Sound Design':
		print('Page has no tables')
		continue

	records = []
	records_alt = []
	# Put them all together
	for table in wq.tables:
		# get regular way
		# data = wq.get_data_from_table(table)
		# records.extend(data)

		# get alt way
		data_alt = methods.get_data_from_table_alt(table)
		records_alt.extend(data_alt)





	# ------------------------------------------------------------------------------

	df = pd.DataFrame(records_alt)
	n_rows_orig, n_cols_orig = df.shape

	# Drop rows which don't have values outside of core
	df.replace({'N/A':np.nan, '—': np.nan}, inplace=True)
	df.drop_duplicates(inplace=True)
	drop_empty_rows = df[df.drop(columns=['year','season','season_link', 'winner']).isna().all(axis=1)].index
	df.drop(drop_empty_rows, inplace=True)

	# If an entire column is null, drop it
	df.dropna(axis=1, how='all', inplace=True)


	# Set year as int and sort
	df['year'] = df['year'].astype(int)
	df.sort_values(by='year', inplace=True)
	df.reset_index(drop=True, inplace=True)


	n_rows_now, n_cols_now = df.shape
	print(f'dropping {n_rows_orig-n_rows_now:,} rows & {n_cols_orig - n_cols_now:,} columns ')

	# df.query('winner and year>1950 and year<2005').shape

	# Do a QA test:
	# Store a query and expected number of results
	test_query_dict = {
		'Tony Award for Best Actor in a Musical':{
			'musical.str.contains("Angel") and year<=2000':3,
			'musical=="Hamilton" and year==2016 and musical_link.notnull()':2,
			'actor=="Lin-Manuel Miranda" and winner==False':2,
			'actor.str.contains("z") and winner==True and year<2020':7,

		},
		'Tony Award for Best Actress in a Musical':{
			'year==1947':0,
			'year==1997': 4,
			'year==2003 and musical=="Hairspray" and actress=="Marissa Jaret Winokur" and winner==True': 1,
			'actress=="Marin Mazzie" and winner==False': 2,
			'musical == "The King and I"':3,
			'actress=="Sutton Foster"':6
			},
		'Tony Award for Best Actor in a Play':{
			'year==1947':2,
			'play=="Dracula"':1,
		},
		'Tony Award for Best Actress in a Play':{
			'year==1947':2,
		},
		'Tony Award for Best Author':{
			'year>1965':0,
			'year==1947':1,
			'author=="Arthur Miller"':2,
			'production.str.contains("!") and year<2020':3,
		},
		'Tony Award for Best Book of a Musical':{
			'winner and year>1950 and year<2005':37,
			'winner==False and year>1950 and year<2015and author.str.contains("a")':95,
		},
		'Tony Award for Best Choreography':{
			'winner and year>1950 and year<2005':54,
		},
		'Tony Award for Best Conductor and Musical Director':{
			'year>1965':0,
			'year==1948':1
		},
		'Tony Award for Best Direction of a Musical':{
			'year==2020':3,
		},
		'Tony Award for Best Direction of a Play':{
			'production=="Indecent" and director=="Rebecca Taichman" and winner == True':1,
		},
		'Tony Award for Best Director':{
			'year>1959':0,
			'year==1947':1,
		},
		'Tony Award for Best Featured Actor in a Play':{
			'year>=1990 and year <=2020 and play.str.startswith("C")':5,
			'year==2020 and play=="Slave Play" and winner==False':2
		},
		'Tony Award for Best Featured Actress in a Play':{
			'actress.astype("str").str.contains("l")':37,
			'work.astype("str").str.contains("o")':46
		},
		'Tony Award for Best Lighting Design':{
			'designer.str.contains("Akerlind")':7,
		}
	}

	if wq.wiki_title in test_query_dict:
		my_queries = test_query_dict.get(wq.wiki_title)
		for q, v in my_queries.items():
			res = df.query(q)
			assert len(res) == v





	# If you want to save
	if os.environ.get('SAVE',True):
	    os.makedirs('data', exist_ok=True)
	    name_root = wq.url.split('/')[-1]
	    df_name = os.path.join('data', f'Wikipedia_scrape_{name_root}.csv')
	    df.to_csv(df_name, index=False)

wq.tables

#
