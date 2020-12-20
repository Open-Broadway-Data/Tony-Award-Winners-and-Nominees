import os
import sys
sys.path.append('scrape_wikipedia')

from scrape_wikipedia import WikiScraper, tony_award_root_url


wq = WikiScraper(tony_award_root_url)

soup = wq.soup

# Next, we find all the links...
all_links = soup.find_all('a')
len(all_links)

all_good_links = soup.select('ul li a[href^="/wiki/Tony_Award_for"][title]')
all_good_links = set(x.get("href") for x in all_good_links)
