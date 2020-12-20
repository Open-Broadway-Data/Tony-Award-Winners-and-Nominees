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


    # Soup on demand
    @property
    def soup(self):
        return utils.get_soup(self.url)

    # tables on demand
    @property
    def tables(self):
        soup = self.soup
        return utils.get_tables_from_url(soup, self.table_attrs)


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # continue here...
    @staticmethod
    def get_links_for_tony_awards(soup):
        """
        Wrapper for `methods.get_data_from_table`
        """
        return methods.get_links_for_tony_awards(soup)




    # continue here...
    @staticmethod
    def get_data_from_table(table):
        """
        Wrapper for `methods.get_data_from_table`
        """
        return methods.get_data_from_table(table)













#
