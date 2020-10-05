from scrape_wikipedia import base_url, WikiScraper
import pandas as pd

if __name__ == "__main__":
    """This does the things we want..."""
    wq = WikiScraper(base_url)
    tables = wq.tables

    df=pd.DataFrame()
    # Currently, tables are extracted successfully
    for table in wq.tables:

        # Need to allow df from tables...
        sub_df = wq.get_df_from_table(table)
        df = df.append(sub_df,ignore_index=True)

    name_root = wq.url.split('/')[-1]
    df_name = 'Wikipedia_scrape_' + name_root + '.csv'
    df = df[['Year','Winner','Musical','Music','Book','Lyrics','Link']]
    print(df)
