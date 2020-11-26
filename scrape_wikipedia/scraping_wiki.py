import os
import re
from . import utils
import requests
from bs4 import BeautifulSoup
import pandas as pd



class WikiScraper:
    """
    This represents the class for scraping wikipedia
    """

    def __init__(self, url, **kwargs):
        self.url = url
        self.table_attrs = kwargs.get("table_attrs", {"class": ["wikitable"]})
        self.soup = utils.get_soup(url)

    @property
    def tables(self):
        return utils.get_tables_from_url(self.soup, self.table_attrs)



    @staticmethod
    def get_data_from_table(table):
        """
        returns a structured table for a beautiful soup table
        """

        # ----------------------------------------------------------------------
        # 1. Get your column names
        my_columns = utils.get_column_names(table)

        # get all values
        records = []
        rows = table.find_all('tr')

        # 2. Iterate through rows.
        for row in rows[1:]:

            # 3. get row indexes
            # get the year and season – then, get out of there...
            index_col = row.find('td', {'rowspan':True})

            # Default values as none...
            year = None; season=None; winner=None;

            if index_col:
                year = int(index_col.find('b').text)
                season = utils.get_text_from_tag(index_col.find('a',{'href':True, 'title':True}),'title')
                continue

            # 4. Is this row a winner?
            # Figure out if they won the tony award or not...
            winning_attrs={'style':'background:#B0C4DE'}
            winner = utils.is_this_a_winner(row, winning_attrs)


            # 5. Initialize record
            # Begin the record....
            rec = {'year':year, 'season': season, 'winner':winner}


            n_cells = len(row.find_all('td'))

            # 6. Iterate through each row (get cell values)
            # i = 1 since index_col is i=0
            i=1
            for cell in row.find_all('td'):

                #how many rows does this cell span?
                n_cols = int(utils.remove_punctuation(cell.get("colspan", 1)))

                for j in range(n_cols):

                    col_name = my_columns[i]
                    val = utils.get_text_from_tag(cell.text)

                    # 7. Store your values
                    rec.update({col_name: val})
                    # get the text

                    # 8. Augement values, if necessary
                    # if there's a link, get the link
                    if cell.find("a", {"href":True}):
                        href = cell.find("a").get("href")
                        href = 'https://en.wikipedia.org' + href
                        rec.update({col_name + "_link": href})


                    # done iterating through this cell...
                    i+=1

            # 9. save your row
            records.append(rec)

        # 10. All done!
        return records






        # ----------------------------------------------------------------------



























# end of page yo...
