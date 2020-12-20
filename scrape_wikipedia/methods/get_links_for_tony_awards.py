from scrape_wikipedia import utils
from scrape_wikipedia import tony_award_root_url

def get_links_for_tony_awards():
    """
    Get the links for wikipedia pages for all Tony Award categories

    returns a list of urls
    """

    soup = utils.get_soup(tony_award_root_url)

    all_links = soup.select('ul li a[href^="/wiki/Tony_Award_for"][title]')
    all_links_urls = list(set(x.get("href") for x in all_links))

    return all_links_urls
