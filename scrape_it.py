import sys
from scrape_wikipedia import base_url, WikiScraper, utils
import pandas as pd

if __name__ == "__main__":
    """This does the things we want..."""
    wq = WikiScraper(base_url)
    tables = wq.tables


    # NEED TO DEBUG THE FOLLOWING CODE!

    records = []

    # Put them all together
    for table in wq.tables:
        data = wq.get_data_from_table(table)
        records.append(data)

    df = pd.DataFrame.from_records(records)

    name_root = wq.url.split('/')[-1]
    df_name = 'Wikipedia_scrape_' + name_root + '.csv'
    df = df[['Year','Winner','Musical','Music','Book','Lyrics','Link']]
    print(df)
