from mordecai import Geoparser
import pandas as pd

def locations_df(csv_file="", sep='\t'):
    '''
    Input: Pandas DataFrame

    Output: Pandas DataFrame w/ locs column
    '''

    def parse_tweet(data, text=False, df_column="Full_Text"):
        '''
        Input: Pandas DataFrame or str

        Output: List of locations for data provided
        '''
        if(text==False):
            locations = geo.geoparse(data[df_column])
        else:
            locations = geo.geoparse(data)

        loc_list = {}
        if locations:
            for loc in locations:
                try:
                    if(loc['country_predicted'] == "USA"):
                        loc_list[loc['geo']['place_name']] = (loc['geo']['lat'], loc['geo']['lon'])
                except:
                    continue

            return loc_list
        else:
            return np.nan

    # Spin up geoparser from mordecai
    try:
        geo = Geoparser()

    except ConnectionRefusedError:
        assert "ConnectionRefusedError: Is the Docker image running?"

    except Exception as e:
        print(e)


    # Map locations to text
    tweet_df = pd.read_csv(csv_file, sep=sep)
    tweet_df['locs'] = tweet_df.apply(parse_tweet, axis = 1)
    return tweet_df
