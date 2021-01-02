import requests
import bs4
from string import punctuation
import re

import pandas as pd

def remove_punctuation(string, exceptions=[]):
    # No need if it's not a string
    if not isinstance(string, str):
        return string

    # Get a list of all the characters you want to remove...
    remove_punct = [x for x in punctuation]

    # Keep exceptions
    for x in exceptions:
        if x in remove_punct:
            remove_punct.remove(x)

    pattern = re.compile('[' + ''.join(remove_punct) +']')
    replaced = re.sub(pattern, '', string)

    return replaced


def get_soup(url):
    # Request the document
    r = requests.get(url)
    html_doc = r.text
    soup = bs4.BeautifulSoup(html_doc,'lxml')
    return soup



# ---------------------------------------------------
def get_number(string):
    """returns a tuple with the text and href of an a tag"""
    return (soup_tag.text, soup_tag.get("href"))



# ---------------------------------------------------

def get_text_from_tag(string:str, attr=None):
    # if isinstance(string, str):
    #     return string.strip()

    if not string:
        return None

    # doesn't always need to look something up...
    if attr:
        string = string.get(attr)

    if hasattr(string, 'text'):
        string = string.text

    return remove_punctuation(string, exceptions=['*', '†']).strip()


# ---------------------------------------------------
def get_links_clean(soup_tag):
    """returns a tuple with the text and href of an a tag"""
    return (soup_tag.text, soup_tag.get("href"))




# ---------------------------------------------------
def is_this_a_winner(row, winning_attrs):
    """
    If your row has all of the winning attributes of the inputted dict, then it's a winner

    returns a boolean value
    """
    for key, value in winning_attrs.items():

        row_value = row.get(key)

        # # If the row has a semicolon but the value doesn't
        # if not value.endswith(';') and row_value.endswith(';'):
        #     row_value=row_value[:-1]

        if row_value and value in row_value:
        # if row_value==value:
            return True
        else:
            return False







#
