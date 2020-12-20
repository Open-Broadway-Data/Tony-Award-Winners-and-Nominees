import os
import sys
sys.path.append('scrape_wikipedia')

from scrape_wikipedia import WikiScraper, tony_award_root_url


wq = WikiScraper(tony_award_root_url)

soup = wq.soup

# Next, we find all the links...
all_links = soup.find_all('a')



#
