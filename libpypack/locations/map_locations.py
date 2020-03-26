from mordecai import Geoparser
import pandas as pd
import numpy as np
import os

def locations_df(csv_file, sep="\t", directory=False, port=9200, host='127.0.0.1', output_filename='parsed_locs.csv', output_dir='', df_column="Full_Text"):
    '''
    Input: Pandas DataFrame

    Output: Pandas DataFrame w/ locs column
    '''
    def parse_tweet(data, geoparser, text=False, USA_Only=True, df_column=df_column):
        '''
        Input: Pandas DataFrame or str

        Output: List of locations for data provided
        '''
        if(text==False):
            locations = geoparser.geoparse(str(data[df_column]))
        else:
            locations = geoparser.geoparse(str(data))

        loc_list = {}

        if locations:
            for loc in locations:
                try:
                    if(USA_Only):
                        if(loc['country_predicted'] == "USA"):
                            loc_list[loc['geo']['place_name']] = (loc['geo']['lat'], loc['geo']['lon'])
                    else:
                        loc_list[loc['geo']['place_name']] = (loc['geo']['lat'], loc['geo']['lon'])
                except:
                    continue

            return loc_list
        else:
            return np.nan

    # Spin up geoparser from mordecai
    try:
        geo = Geoparser(es_port=int(port), es_hosts=(host))

    except Exception as e:
        print(e)
        print('Try running locations.start_docker')
        assert "Geoparser was unable to run, check port and hostname and make sure Docker is running"

    if(directory):
        data_files = os.listdir(csv_file)
        for file in data_files:
            tweet_df = pd.read_csv(csv_file, sep=sep)
            tweet_df['locs'] = tweet_df.apply(parse_tweet, geoparser=geo, axis = 1)
            tweet_df.to_csv(os.path.join(output_dir, file[-4:] + "_mord.csv") + file[-4:], sep='\t')
        return "Process Complete"
    else:
        # Map locations to text
        tweet_df = pd.read_csv(csv_file, sep=sep)
        tweet_df['locs'] = tweet_df.apply(parse_tweet, geoparser=geo, axis = 1)
        tweet_df.to_csv(os.path.join(output_dir, output_filename), sep='\t')
        return tweet_df
