import os
import re

import requests
from bs4 import BeautifulSoup
import numpy as np
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
        """
        self.url = url
        self.table_attrs = kwargs.get("table_attrs", {"class": ["wikitable"]})
        self._soup = None # Set initially to none, this speeds things up.


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #   PROPERTIES
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    @property
    def soup(self):
        """Dynamic loading of a value through clever property and assignment"""
        if not self._soup:
            self._soup = utils.get_soup(self.url)
        return self._soup


    @property
    def wiki_title(self):
        return self.soup.select_one('.firstHeading').text.strip()

    # tables on demand
    @property
    def tables(self):
        return utils.get_tables_from_url(self.soup, self.table_attrs)



    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #   STATIC METHODS
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # continue here...
    def get_links_for_tony_awards(*args):
        """
        Wrapper for `methods.get_data_from_table()`

        Works with an initialized url or not:
            `WikiScraper.get_links_for_tony_awards()`
            `WikiScraper(url).get_links_for_tony_awards()`
        """
        return methods.get_links_for_tony_awards()



    @staticmethod
    def get_data_from_table(table):
        """
        Wrapper for `methods.get_data_from_table()`
        """
        return methods.get_data_from_table(table)



    @staticmethod
    def clean_tony_award_wiki_data(records, print_verbose=False, **kwargs):
        """
        Input a list of records, return a cleaned list of records
        (Probs better to stick to a dataframe...)
        """
        df = pd.DataFrame(records)
        n_rows_orig, n_cols_orig = df.shape

        # Clean values
        df.replace({'N/A':np.nan, '—': np.nan}, inplace=True)

        if kwargs.get('wiki_title') == 'Tony Award for Best Featured Actress in a Play':
            df = methods.etl.etl_wiki_tony_award_best_featured_actress_in_play(df)

        df.drop_duplicates(inplace=True)

        # Drop rows which don't have values outside of core
        drop_index = df[df.drop(columns=['year','season','season_link', 'winner'], errors='ignore').isna().all(axis=1)].index
        df.drop(drop_index, inplace=True)

        # If an entire column is null, drop it
        df.dropna(axis=1, how='all', inplace=True)


        # Set year as int and sort
        df['year'] = df['year'].astype(int)
        df.sort_values(by='year', inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Get new shape
        n_rows_now, n_cols_now = df.shape

        # print if you want
        if print_verbose:
            print(f'dropping {n_rows_orig-n_rows_now:,} rows & {n_cols_orig - n_cols_now:,} columns ')

        return df.to_dict('records')

    @staticmethod
    def validate_tony_award_wiki_data(records, wiki_title):
        """
        Make sure your data is gucci. Doesn't return anything, just passes if okay.

        NOTE: This function is a wrapper for `methods.test_data_quality_tony_awards(records, wiki_title)`

        Also: wiki_title=self.wiki_title
        """
        methods.test_data_quality_tony_awards(records, wiki_title)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #   BLOCK METHODS
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def get_data_from_all_tables(self):
        """
        Returns data from all tables on a wikipedia page as a list of records.
        """
        records = []
        # Put them all together
        for table in self.tables:
        	data = self.get_data_from_table(table)
        	records.extend(data)

        return records









#
