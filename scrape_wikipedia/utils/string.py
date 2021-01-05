"""String manipulations for web scraping"""

import re
from functools import lru_cache
from locale import atof, setlocale, LC_NUMERIC

# set the local
setlocale(LC_NUMERIC, 'en_US.UTF-8')


@lru_cache(maxsize=100)
def get_number_from_str(string:str, n_results='first', coerce_type='int'):
    """
    Returns float from a string

    params:
        string: (str)
        n_results: (str) 'first' for first match, 'all' for all matches

    extract_numbers_from_str('1,000.009 employees\n hi 200', 'first')
    >> 1000.009

    """
    if not string or not string.strip():
        return None

    if n_results=='first':
        matches = re.search('[0-9,.]+', string)
        result = atof(matches.group()) if matches else None
        if coerce_type=='int':
            return int(result)
        else:
            return result

    if n_results=='all':
        matches = re.findall('[0-9,.]+', string)
        result = [atof(x) for x in  matches]
        if coerce_type=='int':
            return list(map(int, result))
        else:
            return result
