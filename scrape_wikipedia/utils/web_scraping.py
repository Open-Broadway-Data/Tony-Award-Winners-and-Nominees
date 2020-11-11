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

def get_links_clean(soup_tag):
    """returns a tuple with the text and href of an a tag"""
    return (soup_tag.text, soup_tag.get("href"))

#records = []
# for row in my_table.find_all('tr')[1:]:
#     rec = {}
#     for i, col in enumerate (row.find_all('td')):
#         #get the column names
#         col_name = col_names[i]
#         #how many rows does this cell span?
#         n_rows = int(col.get("rowspan", 1))
#
#         #this has to be done manually
#         if n_rows == 2:
#             row_1 = col.find("b").text
#             row_2_text, row_2_url = get_links_clean(col.find("a", {"href":True}))
#
#             rec[col_name] = row_1
#             #augmet cell data
#             #this might be giving us our issue
# #             alt_col_name = "Season" if col_name == "Year" else col_name
#             alt_col_name = "Season"
#             rec[alt_col_name] = row_2_text
#             rec[alt_col_name + "_link"] = row_2_url
#         #for all normal cells
#         if n_rows == 1:
#             cell_data = col.text
#             rec[col_name] = cell_data
#             #If there is a link
#             if col.find("a", {"href":True}):
#                 rec[col_name + "_link"] = col.find("a").get("href")
#     #save your row
#     records.append(rec)
#
# print(records)
