"""Use this as a template to run scripts like jupyter notebooks (using Atom's Hydrogen)"""

import os
import sys
sys.path.append('Tony-Award-Winners-and-Nominees')

from scrape_wikipedia import WikiScraper, base_url

# ------------------------------

wq = WikiScraper(base_url)

all_links_1 = wq.get_links_for_tony_awards()
all_links_2 = WikiScraper.get_links_for_tony_awards()

all_links_1==all_links_2


from itertools import groupby
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


all_equal([all_links_1, all_links_2, all_links_1])
#
