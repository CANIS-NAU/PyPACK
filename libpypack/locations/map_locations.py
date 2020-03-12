from mordecai import Geoparser
import pandas as pd
from tqdm import tqdm
import numpy as np
import os

def locations_df(csv_file="", sep='\t', directory=False):
    '''
    Input: Pandas DataFrame

    Output: Pandas DataFrame w/ locs column
    '''
    def parse_tweet(data, text=False, df_column="Full_Text", es_port=9200, es_hosts='127.0.0.1'):
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
        geo = Geoparser(es_port=int(es_port), es_hosts=es_hosts)

    except Exception as e:
        print(e)
        print('Try running locations.start_docker')
        assert "Geoparse was unable to run, check port and hostname and make sure Docker is running"



    if(directory):
        data_files = os.listdir(csv_file)
        for file in data_files:
            tweet_df = pd.read_csv(csv_file, sep=sep)
            tqdm.pandas()
            tweet_df['locs'] = tweet_df.progress_apply(parse_tweet, axis = 1)
            tweet_df.to_csv(file[-4:] + "_mord.csv")
        return "Process Complete"
    else:
        # Map locations to text
        tweet_df = pd.read_csv(csv_file, sep=sep)
        tqdm.pandas()
        tweet_df['locs'] = tweet_df[0:100].progress_apply(parse_tweet, axis = 1)
        return tweet_df

def write_csv(output_dir, file, df, sep='\t'):
    df.to_csv(output_dir + file, sep=sep)
    return 0
