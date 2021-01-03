import pandas as pd

# Store a query and expected number of results
test_query_dict = {
    'Tony Award for Best Actor in a Musical':{
        'musical.str.contains("Angel") and year<=2000':3,
        'musical=="Hamilton" and year==2016 and musical_link.notnull()':2,
        'actor=="Lin-Manuel Miranda" and winner==False':2,
        'actor.str.contains("z") and winner==True and year<2020':7,

    },
    'Tony Award for Best Actress in a Musical':{
        'year==1947':0,
        'year==1997': 4,
        'year==2003 and musical=="Hairspray" and actress=="Marissa Jaret Winokur" and winner==True': 1,
        'actress=="Marin Mazzie" and winner==False': 2,
        'musical == "The King and I"':3,
        'actress=="Sutton Foster"':6
        },
    'Tony Award for Best Actor in a Play':{
        'year==1947':2,
        'play=="Dracula"':1,
    },
    'Tony Award for Best Actress in a Play':{
        'year==1947':2,
    },
    'Tony Award for Best Author':{
        'year>1965':0,
        'year==1947':1,
        'author=="Arthur Miller"':2,
        'production.str.contains("!") and year<2020':3,
    },
    'Tony Award for Best Book of a Musical':{
        'winner and year>1950 and year<2005':37,
        'winner==False and year>1950 and year<2015and author.str.contains("a")':95,
    },
    'Tony Award for Best Choreography':{
        'winner and year>1950 and year<2005':54,
    },
    'Tony Award for Best Conductor and Musical Director':{
        'year>1965':0,
        'year==1948':1
    },
    'Tony Award for Best Direction of a Musical':{
        'year==2020':3,
    },
    'Tony Award for Best Direction of a Play':{
        'production=="Indecent" and director=="Rebecca Taichman" and winner == True':1,
    },
    'Tony Award for Best Director':{
        'year>1959':0,
        'year==1947':1,
    },
    'Tony Award for Best Featured Actor in a Play':{
        'year>=1990 and year <=2020 and play.str.startswith("C")':5,
        'year==2020 and play=="Slave Play" and winner==False':2
    },
    'Tony Award for Best Featured Actress in a Play':{
        # 'winning_actor.astype("str").str.contains("l")':37,
        # 'winning_production.astype("str").str.contains("o")':46
    },
    'Tony Award for Best Lighting Design':{
        'designer.str.contains("Akerlind")':7,
    }
}


def test_data_quality_tony_awards(records, wiki_title):
    if wiki_title not in test_query_dict:
        return

    df = pd.DataFrame(records)

    # get your stored queries
    my_queries = test_query_dict.get(wiki_title)

    # Make sure you get the expected number of results for each query
    for qeury, expected_value in my_queries.items():
        res = df.query(qeury)
        assert len(res) == expected_value










#
