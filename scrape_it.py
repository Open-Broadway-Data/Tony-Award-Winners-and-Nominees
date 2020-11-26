import sys
import os
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
        records.extend(data)

    df = pd.DataFrame(records)

    name_root = wq.url.split('/')[-1]

    # Make a folder for the data we download...
    os.makedirs('data', exist_ok=True)

    # Save it here
    df_name = os.path.join('data', f'Wikipedia_scrape_{name_root}.csv')
    print(f'Saving data to "{df_name}"')


    df['Pulitzer_Prize_Winner'] = df['Musical'].str.contains('†')
    df['Pulitzer_Prize_Finalist'] = df['Musical'].str.contains('\*')

    df.to_csv(df_name)

    # df = df[['Year','Winner','Musical','Music','Book','Lyrics','Link']]
    # print(df)
