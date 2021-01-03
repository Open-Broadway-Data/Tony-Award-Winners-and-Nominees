import pandas as pd

def etl_wiki_tony_award_best_featured_actress_in_play(df):
    """Special case by case basis, clean df for best featured actress in a play"""
    assert isinstance(df, pd.DataFrame)
    assert 'nominees' in df.columns


    df = df.explode('nominees').reset_index(drop=True)

    #Clean up
    df['season'] = df['season_link'].apply(lambda x: x.split('/')[-1].replace('_',' ').lower())
    df.rename(
        columns={
            'actress':'winning_actor',
            'actress_link':'winning_actress_link',
            'role':'winning_role',
            'work':'winning_production',
            'work_link':'winning_production_link'
            },
        inplace=True)

    df_nominee_data = df['nominees'].apply(pd.Series).drop(columns=0).add_prefix('nominee_')
    df = df.merge(df_nominee_data, left_index=True, right_index=True).tail(50)

    # drop what you don't need
    df.drop(columns=['winner', 'nominees'],inplace=True)

    return df
