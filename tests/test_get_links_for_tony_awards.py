import os
import sys
sys.path.append('scrape_wikipedia')

from scrape_wikipedia import methods

def test_get_all_links():

    all_links = methods.get_links_for_tony_awards()
    assert(len(all_links)>0)

if __name__ == '__main__':
    test_get_all_links()
