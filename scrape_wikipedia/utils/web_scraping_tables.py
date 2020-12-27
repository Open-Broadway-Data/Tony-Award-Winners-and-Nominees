import re
import bs4
from string import punctuation
from functools import lru_cache
import pandas as pd


@lru_cache(maxsize=100)
def get_width(string):
    if not string:
        return None
    m = re.match(r'width:(\d{1,3})\%;', string)
    if not m:
        return None
    # otherwise
    return int(m.group(1))



def get_tables_from_url(soup, attrs:dict, filter_width=False):
    """
    Gets a list of tables from an input url.

    attrs: class attributes
    """
    assert (isinstance(soup, bs4.BeautifulSoup))
    # Request the document

    tables = soup.findAll("table", attrs)

    # Allow the user the option of filtering tables by their widths (removes smaller tables)
    if filter_width:
        # Now, filter based on widths
        table_widths = [get_width(x.get('style')) for x in tables]
        val_counts = pd.value_counts(table_widths)

        # 2 or more values and the smaller table is substantially smaller
        if val_counts.sum()!=len(tables) \
            or (len(val_counts)==2 and (val_counts.index[0] - val_counts.index[1])>5):
            # anything that isn't big, delete...
            my_width = val_counts.index[0]

            # Remove small tables as well as those w/o width
            for tb, tb_w in zip(tables, table_widths):
                if not tb_w or tb_w<my_width:
                    tables.remove(tb)

        elif len(val_counts)>2:
            raise ValueError('There are 3 types of tables on this page... Help...')


    return tables


# ---------------------------------------------------

def get_column_names(my_table)-> list:
    '''
    Extract the column names from a wikitable or any html table.

    Params:
        my_table: a bs4 object representing an html table.

    Returns:
        a list of column names.
    ----
    Note: This is a well documented function!!!
    '''
    assert isinstance(my_table, bs4.element.Tag)

    # "th" is a header cell
    # header_rows = my_table.find_all('th')
    header_rows = my_table.select('tr:first-of-type th')
    """
    all wiki tables should have header rows('th')
    but what if it doesn't?
    here is a method to make if fool proof
    """

    if len(header_rows) == 0:
        #'tr' is a row
        all_rows = my_table.find_all('tr')
        #if the table is empty, return an empty list
        if len(all_rows) == 0:
            return []
        header_rows = all_rows[0]

    # clean up text inside cell
    # this method does not change the casing of the column text
    column_names = [x.text.strip() for x in header_rows]

    return column_names
