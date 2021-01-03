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
            'role_link':'winning_role_link',
            'work':'winning_production',
            'work_link':'winning_production_link'
            },
        inplace=True)

    df_nominee_data = df['nominees'].apply(pd.Series).drop(columns=0).add_prefix('nominee_')\
    # Perform a left join (many to one)
    df = df.merge(df_nominee_data, left_index=True, right_index=True)

    # drop what you don't need
    df.drop(columns=['winner', 'nominees', 'ref', 'ref_link', 'nominees_link'],inplace=True)



    # Now some more etl
    new_records = []

    winner_cols = [
    	'year',
    	'season',
    	'season_link',
    	'winning_actor',
    	'winning_actress_link',
    	'winning_role',
    	'winning_role_link',
    	'winning_production',
    	'winning_production_link'
    	]
    winner_cols_map = {
    	'winning_actor':'actor',
    	'winning_actress_link':'actor_link',
    	'winning_role':'role',
    	'winning_role_link':'role_link',
    	'winning_production':'production',
    	'winning_production_link':'production_link'
    }

    df_winners = df[winner_cols].drop_duplicates().rename(columns=winner_cols_map)
    df_winners['winner'] = True
    new_records.extend(df_winners.to_dict('records'))


    nominee_cols = [
    	'year',
    	'season',
    	'season_link',
    	'nominee_actor',
    	'nominee_actor_link',
    	'nominee_role',
    	'nominee_role_link',
    	'nominee_production',
        'nominee_production_link'
    	]

    nominee_cols_map = {
    	'nominee_actor':'actor',
    	'nominee_actor_link':'actor_link',
    	'nominee_role':'role',
    	'nominee_role_link':'role_link',
    	'nominee_production':'production',
        'nominee_production_link':'production_link'
    }

    df_nominees = df[nominee_cols].drop_duplicates().rename(columns=nominee_cols_map)
    df_nominees = df_nominees[df_nominees['actor'].notnull()]
    df_nominees['winner'] = False
    new_records.extend(df_nominees.to_dict('records'))


    df = pd.DataFrame(new_records)
    
    return df
