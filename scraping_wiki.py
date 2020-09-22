import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_tables_from_url(url):
    """
    Gets a list of tables from an input url.

    """

    # Request the document
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc,'lxml')

    table_classes = {"class": ["wikitable"]}
    tables = soup.findAll("table", table_classes)

    return tables



def get_df_from_table(table_in):
    """
    returns a structured table for a beautiful soup table
    """

    ### SET UP REGEX

    re_1 = "\d{4}"
    re_2 = "\d{1,2}(th|rd|st|nd) Tony Awards"

    # Get Winners!
    winner_vals=[]
    for row in table_in.find_all('tr',attrs={'style':'background:#B0C4DE'}):
        vals = [cell.text.strip() for cell in row.findAll('td')]
        winner_vals.append(vals)


    # JUMP INTO IT!
    parsed_table_data=[]
    rows = table_in.find_all('tr')

    row_1 = rows[0]
    variables = [cell.text.strip() for cell in row_1.findAll('th', style=True)]

    record_list = []
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




url = 'https://en.wikipedia.org/wiki/Tony_Award_for_Best_Musical'




tables = get_tables_from_url(url)
df=pd.DataFrame()
for table in tables[:-1]:
    sub_df = get_df_from_table(table)
    df = df.append(sub_df,ignore_index=True)

name_root = url.split('/')[-1]
df_name = 'Wikipedia_scrape_' + name_root + '.csv'
df = df[['Year','Winner','Musical','Music','Book','Lyrics','Link']]
