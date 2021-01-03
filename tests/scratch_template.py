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
	# print(award_type)




	records = wq.get_data_from_all_tables()
	clean_records = wq.clean_tony_award_wiki_data(records, wiki_title=wq.wiki_title)


	# ------------------------------------------------------------------------------

	df = pd.DataFrame(clean_records)






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
			# 'winning_actor.astype("str").str.contains("l")':37,
			# 'winning_production.astype("str").str.contains("o")':46
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
