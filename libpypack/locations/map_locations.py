from mordecai import Geoparser
import pandas as pd
import numpy as np
import os

def locations_df(csv_file, sep="\t", directory=False, port=9200, host='127.0.0.1', output_filename='parsed_locs.csv', output_dir='', df_column="Full_Text"):
    '''
    Pass in a CSV file and recieve another CSV file with locations parsed
    from whatever column is selected for 'column_name'.

    Parameters
    ----------
    csv_file: float / str
              [-90 90] in decimal or DMS (degrees:minutes:seconds)
              Examples: 38.26 or 38:15:36N

    sep: float / str
               [-180 180] in decimal or DMS (degrees:minutes:seconds)
               Examples: -77.51 or 77:30:36W

    directory: boolean
            Examples: True / False

    port: int
            Examples: 8888, Default: 9200

    host: str
            Examples: 127.0.0.1

    port: str
            Examples: 'parsed_locs.csv'

    output_dir: str
            Examples: '/User/Desktop'

    df_column: str
            Examples: 'json' / 'jsonp' / 'xml'


    Returns
    -------
    : dataframe
      Pandas DataFrame with the column 'locs'

    '''

    def parse_tweet(data, geoparser, text=False, USA_Only=True, df_column=df_column):
        """

        A Helper function to locations_df, this function does the parsing of locations
        and outputs the necessary columns/files.

        Parameters
        ----------
        data: str
                  Text data to be parsed for locations.
                  Examples: "Flagstaff is a city in Arizona."

        geoparser: function references
                   Mordecai Geoparser
                   Examples: geo = Geoparser(es_port=int(port), es_hosts=(host))

        text: boolean
                Examples: True / False

        USA_Only: boolean
                Examples: True / False

        df_column: str
                Examples: 127.0.0.1

        Returns
        -------
        : list
          List of locations parsed from a column in the CSV passed in.

        """
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
            tweet_df.to_csv(os.path.join(output_dir, file[-4:] + "_mord.csv") + file[-4:], sep='\t', index=False)
        return "Process Complete"
    else:
        # Map locations to text
        tweet_df = pd.read_csv(csv_file, sep=sep)
        tweet_df['locs'] = tweet_df.apply(parse_tweet, geoparser=geo, axis = 1)
        tweet_df.to_csv(os.path.join(output_dir, output_filename), sep='\t', index=False)
        return tweet_df
