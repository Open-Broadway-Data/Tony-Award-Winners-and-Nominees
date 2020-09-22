from . import base_url, WikiScraper


def do_all():
    """
    This does the things we want...
    """
    wq = WikiScraper(base_url)
    print(wq.url)

    return
    # Desired:
    tables = wq.tables
    df=pd.DataFrame()
    for table in wq.tables:
        sub_df = get_df_from_table(table)
        df = df.append(sub_df,ignore_index=True)

    # name_root = url.split('/')[-1]
    # df_name = 'Wikipedia_scrape_' + name_root + '.csv'
    # df = df[['Year','Winner','Musical','Music','Book','Lyrics','Link']]
