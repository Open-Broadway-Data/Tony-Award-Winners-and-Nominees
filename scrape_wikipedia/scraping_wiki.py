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
            index_row = row.find('td', {'rowspan':True})
            if index_row:
                year = int(index_row.find('b').text)
                season = utils.get_text_clean(index_row.find('a',{'href':True, 'title':True}),'title')
                continue

            # Begin the record....
            rec = {'year':year, 'season': season}


            n_cells = len(row.find_all('td'))

            # Iterate through rows
            for i, cell in enumerate (row.find_all('td')):

                #get the column names
                col_name = my_columns[i]
                print(cell, col_name)
        #
        #         #how many rows does this cell span?
        #         n_rows = int(col.get("rowspan", 1))
        #
        #         #this has to be done manually
        #         if n_rows == 2:
        #             row_1 = col.find("b").text
        #             row_2_text, row_2_url = utils.get_links_clean(col.find("a", {"href":True}))
        #
        #             rec[col_name] = row_1
        #             # augmet cell data
        #             #this might be giving us our issue
        # #             alt_col_name = "Season" if col_name == "Year" else col_name
        #             alt_col_name = "Season"
        #             rec[alt_col_name] = row_2_text
        #             rec[alt_col_name + "_link"] = row_2_url
        #
        #
        #         #for all normal cells
        #         if n_rows == 1:
        #             cell_data = col.text
        #             rec[col_name] = cell_data
        #             #If there is a link
        #             if col.find("a", {"href":True}):
        #                 rec[col_name + "_link"] = col.find("a").get("href")
        #     # save your row
        #     records.append(rec)
        # print(records)
        return

        # JUMP INTO IT!
        parsed_table_data=[]


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






        # ----------------------------------------------------------------------

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
