import os
import json
import datetime

from scrape_wikipedia import utils
from scrape_wikipedia import tony_award_root_url
from scrape_wikipedia.wiki_scraper import WikiScraper

def get_links_for_tony_awards():
    """
    Get the links for wikipedia pages for all Tony Award categories

    returns a list of urls
    """

    soup = utils.get_soup(tony_award_root_url)

    all_links = soup.select('ul li a[href^="/wiki/Tony_Award_for"][title]')
    all_links_urls = set(x.get("href") for x in all_links)
    all_links_urls_formatted = list(map(lambda x: 'https://wikipedia.org'+x, all_links_urls))

    # sort them
    sorted(all_links_urls_formatted)

    return all_links_urls_formatted





# ------------------------------------------------------------------------------

# This helpful function makes life a bit easier...
def get_dict_of_links_for_tony_awards(save=True):
    """
    Returns a dictionary (sorted by key), representing links for wikipedia pages for all Tony Award
    categories. Dict keys are Tony Award categories, values are the URL.

    Params:
        save: (default True) saves a json of the dict locally for faster loading,
        especially helpful when testing.
    """

    # File path....
    if save:
        # Store the stuff here
        os.makedirs('data/internal', exist_ok=True)

    file_path = 'data/internal/all_tony_award_wikipedia_links.json'

    # If you have it, reload it...
    if os.path.isfile(file_path):

        # Check to see if it's created more recently than 1 week ago
        dt_created = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        one_week_ago = datetime.datetime.now() - datetime.timedelta(weeks=1)

        # Created earlier than 1 week ago?
        if dt_created > one_week_ago:
            # Nice and fresh, load and send
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data


    all_links = get_links_for_tony_awards()

    # Do this once...
    data = {}

    # Go through each url – set ensure they are unique
    for link in set(all_links):

        wq = WikiScraper(link)
        award_type = wq.wiki_title

        data[link] = award_type

    # Reverse the dict
    data_r = {}
    for key, value in data.items():

        # If the value already exists, it's a redirect. Choose the shorter url
        if value in data_r:
            if len(key) < len(data_r[value]):
                data_r[value] = key
            continue

        # Otherwise, set the value and move on
        data_r[value] = key

    # Now sort
    data_r_sorted = {k:v for k,v in sorted(data_r.items())}


    # Save for future use
    if save:
        with open(file_path, 'w') as f:
            json.dump(data_r_sorted, f)

    # Now return
    return data_r_sorted
