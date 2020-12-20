from scrape_wikipedia import utils
import bs4

def get_links_for_tony_awards(soup:bs4.BeautifulSoup):
    """
    Get the links for wikipedia pages for all Tony Award categories

    returns a list of urls
    """
    
    all_links = soup.select('ul li a[href^="/wiki/Tony_Award_for"][title]')
    all_links_urls = set(x.get("href") for x in all_links)

    return all_links_urls
