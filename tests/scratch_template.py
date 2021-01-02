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
- [ ]	Tony Award for Best Featured Actress in a Play  <-------- This one will need work. It has a non-standard format. Consider revising directly on Wikipedia...
- [ ]	Tony Award for Best Lighting Design <-------- Has data for best play and best musical on the same page...
- [X]	Tony Award for Best Lighting Design in a Musical
- [X]	Tony Award for Best Lighting Design in a Play
- [X]	Tony Award for Best Musical
- [X]	Tony Award for Best Newcomer
- [X]	Tony Award for Best Orchestrations
- [X]	Tony Award for Best Original Score
- [X]	Tony Award for Best Play
- [X]	Tony Award for Best Revival
- [ ]	Tony Award for Best Revival of a Musical <------ Need to reconcile values which span multiple rows... (Create a map of indixes to values... This can potentially be used to solve index col issues)
- [X]	Tony Award for Best Revival of a Play
- [X]	Tony Award for Best Scenic Design
- [X]	Tony Award for Best Scenic Design in a Musical
- [X]	Tony Award for Best Scenic Design in a Play
- [ ]	Tony Award for Best Sound Design <------ No tables on this page... Need to go and create them
- [X]	Tony Award for Best Special Theatrical Event
- [ ]	Tony Award for Best Stage Technician <------ Need to reconcile values which span multiple rows
"""


# Continue here -- Getting errors when parsing the individual table
next_key = 'Tony Award for Best Actor in a Musical'

# for next_key in list(all_links_dict.keys())[:13]:

wq = WikiScraper(all_links_dict[next_key])
award_type = wq.wiki_title
print(award_type)

records = []
records_alt = []
# Put them all together
for table in wq.tables:
	# get regular way
	data = wq.get_data_from_table(table)
	records.extend(data)

	# get alt way
	data_alt = methods.get_data_from_table_alt(table)
	records_alt.extend(data_alt)

df = pd.DataFrame(records_alt)
df.drop_duplicates(inplace=True)
df.replace({'N/A':None}, inplace=True)
df.sort_values(by='year', inplace=True)

drop_empty_rows = df[df.drop(columns=['year','season','season_link', 'winner']).isna().all(axis=1)].index
df.drop(drop_empty_rows, inplace=True)
df.reset_index(drop=True, inplace=True)




# col_names = [utils.get_text_from_tag(x.text) for x in new_table[0]]


# Pre-populate a list of desired length – faster than a blank list and appending...
# records = [None for _ in range(len(new_table)-1)]
#
# for row_idx, row in enumerate(new_table[1:]):
#
# 	year = utils.get_number_from_str(row[0].select_one('b').text)
# 	season = row[0].select_one('a').text
# 	season_link = row[0].select_one('a[href]')
# 	if season_link:
# 		season_link = season_link.get('href')
#
# 	rec = dict(
# 		year=year,
# 		season=season,
# 		season_link=season_link
# 	)
#
# 	# Go through each of the cells and add the value
# 	for i, cell in enumerate(row[1:]):
# 		if not cell:
# 			continue
# 		my_col = col_names[i+1]
# 		rec[my_col] = cell.get_text(strip=True)
# 		# if there's a link, save it
# 		if cell.select_one('a[href]'):
# 			rec[my_col + '_link'] = cell.select_one('a[href]').get('href')
#
# 	# Save your record
# 	records[row_idx] = rec

pd.DataFrame(records)

row = new_table[4]

rec

col_name = my_columns[i]
val = utils.get_text_from_tag(cell.text)

# 7. Store your values
rec.update({col_name: val})
# get the text

# 8. Augement values, if necessary
# if there's a link, get the link
if cell.find("a", {"href":True}):
	href = cell.find("a").get("href")
	href = 'https://en.wikipedia.org' + href
	rec.update({col_name + "_link": href})







# ------------------------------------------------------------------------------
df = pd.DataFrame(records)

n_rows_orig, n_cols_orig = df.shape


# Drop anything without a year and season
drop_index = df[df[['year', 'season']].isna().sum(axis=1)==2].index

# Now drop
df.drop(drop_index, inplace=True)
df['year'] = df['year'].astype(int)
df.sort_values('year', inplace=True)

# If an entire column is null, drop it
df.dropna(axis=1, how='all', inplace=True)

n_rows_now, n_cols_now = df.shape
print(f'dropping {n_rows_orig-n_rows_now:,} rows & {n_cols_orig - n_cols_now:,} columns ')

# Replace nonsense values
df.replace('—',np.nan, inplace=True)

# Do a QA test:
# Store a query and expected number of results
test_query_dict = {
	'Tony Award for Best Actress in a Musical':{
		'year==1947':0,
		'year==2003 and Musical=="Hairspray" and Actress=="Marissa Jaret Winokur" and winner==True': 1,
		'Musical == "The King and I"':3,
		'Actress=="Sutton Foster"':6
		},
	'Tony Award for Best Actor in a Play':{
		'year==1947':2,
		'Play=="Dracula"':1,
	},
	'Tony Award for Best Actress in a Play':{
		'year==1947':2,
	},
	'Tony Award for Best Author':{
		'year>1965':0,
		'year==1947':1
	},
	'Tony Award for Best Conductor and Musical Director':{
		'year>1965':0,
		'year==1948':1
	},
	'Tony Award for Best Direction of a Musical':{
		'year==2020':3,
	},
	'Tony Award for Best Direction of a Play':{
		'Production=="Indecent" and Director=="Rebecca Taichman" and winner == True':1,
	},
	'Tony Award for Best Director':{
		'year>1959':0,
		'year==1947':1,
	},
	'Tony Award for Best Featured Actor in a Play':{
		'year>=1990 and year <=2020 and Play.str.startswith("C")':5,
		'year==2020 and Play=="Slave Play" and winner==False':2
	},
	'Tony Award for Best Lighting Design':{
		'Designer.str.contains("Akerlind")':7,
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
