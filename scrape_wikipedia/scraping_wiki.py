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
    def get_df_from_table(table):
        """
        returns a structured table for a beautiful soup table
        """

        ### SET UP REGEX

        re_1 = "\d{4}"
        re_2 = "\d{1,2}(th|rd|st|nd) Tony Awards"

        # Get Winners!
        winner_vals=[]
        for row in table.find_all('tr',attrs={'style':'background:#B0C4DE'}):
            vals = [cell.text.strip() for cell in row.findAll('td')]
            winner_vals.append(vals)


        # JUMP INTO IT!
        parsed_table_data=[]
        rows = table.find_all('tr')

        row_1 = rows[0]
        variables = [cell.text.strip() for cell in row_1.findAll('th', style=True)]

        record_list = []
        year = None
        for row in rows[1:]:
            record = {}
            # Add the year
            if re.findall(re_2, row.text):
                year = re.findall(re_1, row.text)[0]
                continue
            values = [cell.text.strip() for cell in row.findAll('td')]

            # Compare to winners
            if values in winner_vals:
                record['Winner']=True
            else:
                record['Winner']=False

            # Get busy
            values.insert(0, year)
            while len(values)< len(variables):
                values.append(values[-1])
            for k, v in zip(variables,values):
                record[k]=v

            if row.find('a'):
                record['Link'] = 'https://en.wikipedia.org' + row.find('a').get('href')

            record_list.append(record)

        df = pd.DataFrame(record_list)
        return df



# if __name__ == "__main__":

    # url = 'https://en.wikipedia.org/wiki/Tony_Award_for_Best_Musical'
    #
    # soup = utils.get_soup('https://en.wikipedia.org/wiki/Tony_Award_for_Best_Musical')
    # attrs = {"class": ["wikitable"]}
    # tables = get_tables_from_url(soup, attrs)
    # print(tables)
