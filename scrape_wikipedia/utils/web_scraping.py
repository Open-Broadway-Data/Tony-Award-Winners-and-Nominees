import requests
from bs4 import BeautifulSoup

def get_soup(url):
    # Request the document
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc,'lxml')
    return soup



def get_tables_from_url(soup, attrs:dict):
    """
    Gets a list of tables from an input url.

    attrs: class attributes
    """
    assert (isinstance(soup, BeautifulSoup))
    # Request the document
    tables = soup.findAll("table", attrs)

    return tables
