import os
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd

# custom stuff
from scrape_wikipedia import utils
from scrape_wikipedia import methods


# ------------------------------------------------------------------------------

class WikiScraper:
    """
    This represents the class for scraping wikipedia
    """

    def __init__(self, url, **kwargs):
        """
        Here are the params:
            url: the url to be scraped
            table_attrs: what is the table attributes for this url
            soup: beautiful soup for this url...
        """
        self.url = url
        self.table_attrs = kwargs.get("table_attrs", {"class": ["wikitable"]})
        self.soup = utils.get_soup(self.url)

    # Soup on demand
    # @property
    # def soup(self):
    #     """Only get soup when you need it..."""
    #     self._soup = utils.get_soup(self.url)
    #     return self._soup

    @property
    def wiki_title(self):
        return self.soup.select_one('.firstHeading').text.strip()

    # tables on demand
    @property
    def tables(self):
        return utils.get_tables_from_url(self.soup, self.table_attrs)



    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # continue here...
    def get_links_for_tony_awards(*args):
        """
        Wrapper for `methods.get_data_from_table`

        Works with an initialized url or not:
            `WikiScraper.get_links_for_tony_awards()`
            `WikiScraper(url).get_links_for_tony_awards()`
        """
        return methods.get_links_for_tony_awards()




    # continue here...
    @staticmethod
    def get_data_from_table(table):
        """
        Wrapper for `methods.get_data_from_table`
        """
        return methods.get_data_from_table(table)













#
