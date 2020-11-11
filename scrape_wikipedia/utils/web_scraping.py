import requests
import bs4

def get_soup(url):
    # Request the document
    r = requests.get(url)
    html_doc = r.text
    soup = bs4.BeautifulSoup(html_doc,'lxml')
    return soup



def get_tables_from_url(soup, attrs:dict):
    """
    Gets a list of tables from an input url.

    attrs: class attributes
    """
    assert (isinstance(soup, bs4.BeautifulSoup))
    # Request the document
    tables = soup.findAll("table", attrs)

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
    header_rows = my_table.find_all('th')

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

# ---------------------------------------------------

def get_text_clean(string, attr=None):
    if not string:
        return None

    # doesn't always need to look something up...
    if attr:
        string = string.get(attr)
    return string.strip()


# ---------------------------------------------------
def get_links_clean(soup_tag):
    """returns a tuple with the text and href of an a tag"""
    return (soup_tag.text, soup_tag.get("href"))












#
