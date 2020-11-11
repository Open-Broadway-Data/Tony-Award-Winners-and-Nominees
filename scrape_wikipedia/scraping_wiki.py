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
        # STEP 1: Determine the year of the table (which tony awards is it referring to?)
        ### We don't really need this. Skip it for now, perhaps get back to it later.



        # ----------------------------------------------------------------------

        # STEP 2: Determine table columns
        ### SET UP REGEX

        my_columns = utils.get_column_names(table)



        # ----------------------------------------------------------------------
        # STEP 3: Determine columns attributes? (some columns aren't columns, but color differences)

        # def get_year_of_row(row):
        #     """specific to tony award wikipedia tables"""
        #
        #     re_1 = "\d{4}"
        #     re_2 = "(\d{1,2}th|rd|st|nd) Tony Awards"
        #
        #     if re.findall(re_2, row):
        #         year = re.findall(re_1, row)[0]
        #         return int(year)
        #     else:
        #         return None




        # ----------------------------------------------------------------------
        # STEP 4: Loop through and get the values


        """
        Ideally you loop through the table's rows and generate value pairs as such:

        records = []
        for row in table:
            rec = {}
            for col in columns:
                rec[col] = value
            # after looping through
            records.append(rec)

        # finally, you are done
        df = pd.DataFrame.from_records(records)
        """


        # get all values
        records = []
        rows = table.find_all('tr')

        for row in rows[1:]:

            # get the year and season – then, get out of there...
            index_col = row.find('td', {'rowspan':True})
            if index_col:
                year = int(index_col.find('b').text)
                season = utils.get_text_clean(index_col.find('a',{'href':True, 'title':True}),'title')
                continue


            # Figure out if they won the tony award or not...
            winning_attrs={'style':'background:#B0C4DE'}
            winner = utils.is_this_a_winner(row, winning_attrs)


            # Begin the record....
            rec = {'year':year, 'season': season, 'winner':winner}


            n_cells = len(row.find_all('td'))

            # Iterate through rows
            # i = 1 since index_col is i=0
            i=1
            for cell in row.find_all('td'):

                #how many rows does this cell span?
                n_cols = int(cell.get("colspan", 1))

                for j in range(n_cols):

                    col_name = my_columns[i]
                    val = utils.get_text_clean(cell.text)

                    rec.update({col_name: val})
                    # get the text

                    # if there's a link, get the link
                    if cell.find("a", {"href":True}):
                        href = cell.find("a").get("href")
                        href = 'https://en.wikipedia.org' + href
                        rec.update({col_name + "_link": href})

                    i+=1
                    # done iterating through this cell...

            # save your row
            records.append(rec)
        return records






        # ----------------------------------------------------------------------



























# end of page yo...
